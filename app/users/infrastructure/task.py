from uuid import UUID

from celery import shared_task


@shared_task(name='sync_contacts')
def sync_contacts(user: UUID):
    from config.dependencies import container

    use_case = container.users.sync_contacts_user_use_case()
    use_case.execute(user)
