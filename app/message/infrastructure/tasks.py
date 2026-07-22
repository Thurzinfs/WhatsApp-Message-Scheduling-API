from uuid import UUID

from celery import shared_task

from app.message.domain.role import StatusMessage


@shared_task(name='check_message_schedule')
def check_message_schedule():
    from config.dependencies import container

    repo = container.messages.message_repo()

    task = container.messages.send_task_adapter()

    use_case = container.messages.list_messages_schedule()
    messages = use_case.execute()

    for schedule in messages:

        schedule.change_status(StatusMessage.process)
        repo.save(schedule)

        task.send_message(schedule.id)


@shared_task(name='send_message')
def send_message(id: UUID):
    from config.dependencies import container

    use_case = container.messages.send_message_use_case()
    use_case.execute(id)
