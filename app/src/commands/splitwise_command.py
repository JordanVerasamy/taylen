import logging

from django.conf import settings
from slack import WebClient
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser

from app.models import User
from app.src.commands.common import CommandException

logger = logging.getLogger('default')

help_message = """```
Creates an expense on splitwise for the specified amount between the two parties.

Usage: 
> .sw <amount> <direction> <user> <description...>

Arguments:
- amount: a money like string
- direction: to or from
- user: @ the user
- description: some words

Examples:
> .sw $4.20 to @tso for pizza
> .sw $69 from @tso for using these meme numbers in their help messages
```"""


class SplitwiseCommand:
    @staticmethod
    async def handle_discord(message):
        logger.info("")

    @staticmethod
    def handle_slack(client: WebClient, event: dict, amount: float, direction: str, recipient: str, description: str):
        logger.info(f"[recipient={recipient}] [direction={direction}] [amount={amount}] [description={description}]")

        try:
            if direction == 'to':
                _create_expense(event['user'], recipient, amount, description)
            elif direction == 'from':
                _create_expense(recipient, event['user'], amount, description)
            else:
                raise CommandException('Invalid direction')

            client.reactions_add(
                name='white_check_mark',
                channel=event['channel'],
                timestamp=event['ts']
            )
        except CommandException:
            client.reactions_add(
                name='x',
                channel=event['channel'],
                timestamp=event['ts']
            )


sObj = Splitwise(settings.SPLITWISE_CONSUMER_KEY, settings.SPLITWISE_CONSUMER_SECRET)
sObj.setAccessToken({
    'oauth_token': settings.SPLITWISE_OUATH_TOKEN,
    'oauth_token_secret': settings.SPLITWISE_OUATH_TOKEN_SECRET
})


def _create_expense(initiator_id: str, recipient_id: str, amount: float, description: str):
    """
    This will create an expense where the {initiator} owes the {recipient} {amount}.
    """
    if amount <= 0:
        raise CommandException('Negative amounts not allowed')

    tso: User = User.objects.get(friendly_name='tso')
    initiator: User = User.objects.get(slack_id=initiator_id)
    recipient: User = User.objects.get(slack_id=recipient_id)
    users = []

    expense = Expense()
    expense.setGroupId(settings.SPLITWISE_GROUP_ID)
    expense.setDescription(description)
    expense.setCost(amount)

    initiator_user = ExpenseUser()
    initiator_user.setId(initiator.splitwise_id)
    initiator_user.setPaidShare(0)
    initiator_user.setOwedShare(amount)
    users.append(initiator_user)

    recipient_user = ExpenseUser()
    recipient_user.setId(recipient.splitwise_id)
    recipient_user.setPaidShare(amount)
    recipient_user.setOwedShare(0)
    users.append(recipient_user)

    # We do this because we're using my access token.
    if tso.id not in [initiator.id, recipient.id]:
        tso_user = ExpenseUser()
        tso_user.setId(tso.splitwise_id)
        tso_user.setPaidShare(0)
        tso_user.setOwedShare(0)
        users.append(tso_user)

    expense.setUsers(users)
    if not sObj.createExpense(expense):
        raise CommandException('Failed to create SW expense')
