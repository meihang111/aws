import tkinter
import logging
import boto3
from botocore.exceptions import ClientError

sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/576764713538/MYQueue"

window = tkinter.Tk()
window.geometry("300x300")
window.title("send")

t = tkinter.Text(window)
t.place(x=10, y=10, height=250, width=280)

var = tkinter.StringVar()
e = tkinter.Entry(window,textvariable=var)
e.place(x=10, y=260, height=30, width=230)


def button_clicked():
    t.insert(tkinter.END, var.get()+'\n')
    msg_body = var.get()
    msg = send_sqs_message(sqs_queue_url, msg_body)
    if msg is not None:
        logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
    e.delete('0', 'end')


m_button = tkinter.Button(window, text='发送', command=button_clicked)
m_button.place(x=240, y=260, height=30, width=50)


def send_sqs_message(sqs_queue_url, msg_body):
    """

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    sqs_client = boto3.client('sqs',region_name="us-east-1")
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=msg_body)
    except ClientError as e:
        logging.error(e)
        return None
    return msg


def main():
    window.mainloop()


if __name__ == '__main__':
    main()