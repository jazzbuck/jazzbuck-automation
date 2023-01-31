import imaplib
import email
import email.utils
import datetime


def connect_to_imap_server(
    username: str,
    password: str,
    imap_server: str,
) -> imaplib.IMAP4_SSL:
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)

    return imap


def retrieve_latest_emails(
    connection: imaplib.IMAP4_SSL,
    n_latest: int,
    expected_sender: str,
    keyword: str = "todo",
) -> list:

    imap = connection
    _, messages = imap.select("INBOX")
    mailbox_messages = int(messages[0])
    list_of_messages = []
    for i in range(max(mailbox_messages - n_latest + 1, 1), mailbox_messages + 1):
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
                                    body = part.get_payload(decode=True).decode(
                                        "utf-8"
                                    )  # decode
                                    break
                        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                        else:
                            body = msg.get_payload(decode=True).decode("utf-8")

                        list_of_messages.append((date, subject, body))

    imap.logout()

    return list_of_messages


def write_todo_email_to_markdown(
    list_of_messages: list[tuple[datetime.datetime, str, str]],
) -> list[tuple[str, str]]:
    list_of_markdown = []

    if list_of_messages:
        for message in list_of_messages:
            dt = format(message[0], "%Y%m%d%H%M")
            date = format(message[0], "%Y-%m-%d")
            subject = message[1]
            if "due:" in subject:
                _, _, after = subject.partition("due:")
                after = after.strip()
                after = after.split()
                if after[0].lower() == "today":
                    date = format(datetime.datetime.now(), "%Y-%m-%d")
                elif after[0].lower() == "tomorrow":
                    date = format(
                        datetime.datetime.now() + datetime.timedelta(days=1), "%Y-%m-%d"
                    )
                else:
                    date = after[0]

            markdown = f"""---
id: {dt}
aliases: ["{dt}","{dt}: {message[1]}"]
sr-due: {date}
sr-interval: 3
sr-ease: 250
---
#todo
```button
name Mark complete
type line(8) template
action done
replace [8,8]
remove true
```

# {message[1]}

{message[2]}"""
            title = message[1]
            title = "".join(x for x in title.title() if not x.isspace())
            title = "".join(x for x in title if x.isalnum())
            title = dt + "-" + title

            list_of_markdown.append((title, markdown))

    return list_of_markdown


def archive_emails_from_inbox(
    connection: imaplib.IMAP4_SSL,
    expected_sender: str,
    keyword: str = "todo",
) -> None:
    imap = connection
    imap.select("INBOX", readonly=False)

    target_inbox = "".join(x for x in keyword if x.isalnum()) + "-archive"

    _, msgs = imap.search(None, f'(SUBJECT "{keyword}")')
    msg_ids = msgs[0].decode().split()

    for msg_id in msg_ids:
        resp_code, response = imap.copy(msg_id, f"{target_inbox}")
        if resp_code == "OK":
            imap.store(msg_id, "+FLAGS", "\\Seen")
            imap.store(msg_id, "+FLAGS", "\\Deleted")

    resp_code, response = imap.expunge()

    imap.logout()

    return None
