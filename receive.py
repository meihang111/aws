import tkinter
import logging
import boto3
from botocore.exceptions import ClientError

sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/576764713538/MYQueue"
num_messages = 1

window = tkinter.Tk()
window.geometry("300x300")
window.title("receive")

t = tkinter.Text(window)
t.place(x=10, y=10, height=250, width=280)


def button_clicked():
    msgs = retrieve_sqs_messages(sqs_queue_url, num_messages)
    if msgs is not None:
        for msg in msgs:
            logging.info(f'SQS: Message ID: {msg["MessageId"]}, '
                         f'Contents: {msg["Body"]}')
            print(msg["Body"])
            # Remove the message from the queue
            delete_sqs_message(sqs_queue_url, msg['ReceiptHandle'])
        t.insert(tkinter.END, (msg["Body"])+'\n')
    else:
        print("暂无消息"+'\n')


m_button = tkinter.Button(window, text='接受下一条消息', command=button_clicked)
m_button.place(x=10, y=260, height=30, width=280)


def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=0, visibility_time=5):
    """Retrieve messages from an SQS queue

    The retrieved messages are not deleted from the queue.

    :param sqs_queue_url: String URL of existing SQS queue
    :param num_msgs: Number of messages to retrieve (1-10)
    :param wait_time: Number of seconds to wait if no messages in queue
    :param visibility_time: Number of seconds to make retrieved messages
        hidden from subsequent retrieval requests
    :return: List of retrieved messages. If no messages are available, returned
        list is empty. If error, returns None.
    """

    # Retrieve messages from an SQS queue
    sqs_client = boto3.client('sqs', region_name="us-east-1")
    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                          MaxNumberOfMessages=num_msgs,
                                          WaitTimeSeconds=wait_time,
                                          VisibilityTimeout=visibility_time)
    except ClientError as e:
        logging.error(e)
        return None

    # Return the list of retrieved messages
    return msgs['Messages']


def delete_sqs_message(sqs_queue_url, msg_receipt_handle):
    """Delete a message from an SQS queue

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_receipt_handle: Receipt handle value of retrieved message
    """

    # Delete the message from the SQS queue
    sqs_client = boto3.client('sqs',region_name="us-east-1")
    sqs_client.delete_message(QueueUrl=sqs_queue_url,
                              ReceiptHandle=msg_receipt_handle)


def main():
    window.mainloop()


if __name__ == '__main__':
    main()