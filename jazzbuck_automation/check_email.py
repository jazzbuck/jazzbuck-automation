import imaplib
import email
import email.utils


def connect_to_imap_server(
    username: str,
    password: str,
    imap_server: str,
) -> imaplib.IMAP4_SSL:
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)

    return imap


def retrieve_latest_emails(
    n_latest: int,
    connection: imaplib.IMAP4_SSL,
    expected_sender: str,
    keyword: str = "todo",
) -> list:
    imap = connection

    _, messages = imap.select("INBOX")
    mailbox_messages = int(messages[0])
    list_of_messages = []
    for i in range(mailbox_messages - n_latest + 1, mailbox_messages + 1):
        _, msg_data = imap.fetch(str(i), "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode("utf-8"))
                sender = msg["from"]
                subject = msg["subject"]
                date = email.utils.parsedate_to_datetime(msg["Date"])
                if keyword in subject:
                    if expected_sender in sender:
                        if msg.is_multipart():
                            for part in msg.walk():
                                ctype = part.get_content_type()
                                cdispo = str(part.get("Content-Disposition"))

                                # skip any text/plain (txt) attachments
                                if ctype == "text/plain" and "attachment" not in cdispo:
                                    body = part.get_payload(decode=True)  # decode
                                    break
                        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                        else:
                            body = msg.get_payload(decode=True)

                        list_of_messages.append((date, subject, body))

    return list_of_messages


def write_todo_email_to_markdown(
    list_of_messages: list[tuple[datetime.datetime, str, str]],
) -> list[tuple[str, str]]:
    list_of_markdown = []

    for message in list_of_messages:
        dt = format(message[0], "%Y%m%d%H%M")
        markdown = f"""---
id: {dt}
aliases: ["{dt},"{dt}: {message[1]}]
---
#todo

# {message[1]}

{message[2]}"""
        title = message[1]
        title = "".join(x for x in title.title() if not x.isspace())
        title = "".join(x for x in title if x.isalnum())
        title = dt + "-" + title

        list_of_markdown.append((title, markdown))

    return list_of_markdown
