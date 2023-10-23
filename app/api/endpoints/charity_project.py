from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_closed_or_invested,
    check_charity_project_exists,
    check_charity_project_fully_invested,
    check_name_duplicate,
    check_correct_full_amount_for_update
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectUpdate,
    CreateCharityProject,
)
from app.services.investment import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CreateCharityProject,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    new_project = await investment_process(new_project, session)

    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_charity_project_exists(project_id, session)
    charity_project = await charity_project_crud.get(project_id, session)
    await check_charity_project_closed_or_invested(charity_project)

    charity_project = await charity_project_crud.remove(
        charity_project, session
    )

    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_charity_project_exists(project_id, session)
    charity_project = await charity_project_crud.get(
        project_id,
        session,
    )
    check_charity_project_fully_invested(charity_project)

    if obj_in.full_amount is not None:
        await check_correct_full_amount_for_update(
            project_id, session, obj_in.full_amount
        )
    if obj_in.name is not None:
        await check_name_duplicate(
            obj_in.name,
            session,
        )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )

    return charity_project
