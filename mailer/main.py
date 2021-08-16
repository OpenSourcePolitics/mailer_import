from sendinblue import Sendinblue
from mailjet import Mailjet
from sql_handling import fill_database
from settings import init


# Call for Sendinblue
mailer = Sendinblue()
mailer.get_mails(
    senders=[os.getenv("SENDERS_SIB")]
)

# Call for Mailjet
init()
mailer = Mailjet()
mailer_data = mailer.get_mails(
    senders=[os.getenv("SENDERS_MJ")]
)
fill_database({'mails': mailer_data})