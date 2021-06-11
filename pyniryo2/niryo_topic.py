import roslibpy
from threading import Event
from pyniryo2.exceptions import TopicException


class NiryoTopic(object):
    """
    Represent a Ros Topic instance. It supports both the request of a single value and/or callbacks.
    """

    def __init__(self, client, topic_name, topic_type):
        """

        :param client: Instance of the ROS connection.
        :type client: roslibpy.Ros
        :param topic_name: Topic name.
        :type topic_name: string
        :param topic_type: Topic type.
        :type topic_type: string
        """
        self.__topic_name = topic_name
        self.__topic_type = topic_type
        self.__topic = roslibpy.Topic(client, self.__topic_name, self.__topic_type)

        self.__user_callback = None

        self.__timeout = 0.5

        self.__sync_topic_value = None
        self.__sync_event = Event()
        self.__sync_event.clear()

    def __del__(self):
        self.unsubscribe()

    def __call__(self):
        if self.__topic.is_subscribed:
            self.__sync_event.wait(timeout=self.__timeout)
            return self.sync_topic_value

        self.sync_topic_value = None
        self.__sync_event.clear()
        self.__topic.subscribe(self.__internal_callback)
        self.__sync_event.wait(timeout=self.__timeout)
        self.__topic.unsubscribe()
        return self.sync_topic_value

    def __str__(self):
        return "Name: {}\nType: {}\nSubscribed: {}\nValue: {}".format(self.__topic_name, self.__topic_type,
                                                                      self.__topic.is_subscribed,
                                                                      self.__sync_topic_value)

    def __repr__(self):
        return self.__str__()

    @property
    def is_subscribed(self):
        return self.__topic.is_subscribed

    @property
    def value(self):
        return self.__call__()

    def subscribe(self, callback):
        """
        Subscribe a callback to the topic. A TopicException will be thrown if the topic is already subscribed.

        :param callback: The callback function which is called at each incoming topic message.
        :type callback: function(dict, )
        :return: None
        :rtype: None
        """
        if not callback:
            raise TopicException("Empty callback on {} topic subscription".format(self.__topic_name))

        if not self.__topic.is_subscribed:
            self.__user_callback = callback
            self.__sync_event.clear()
            self.__topic.subscribe(self.__internal_callback)
        else:
            raise TopicException("Topic {} already subscribed".format(self.__topic_name))

    def unsubscribe(self):
        """
        Unsubscribe to the topic.

        :return:
        :rtype:
        """
        if self.__topic.is_subscribed:
            self.__topic.unsubscribe()
            self.__user_callback = None

    def __internal_callback(self, topic_value):
        """
        This function is an internal callback that stores the last value of the subject
        and calls the user's callback if it is registered.

        :param topic_value: Message returned by the topic.
        :type topic_value: dict
        :return: None
        :rtype: None
        """
        self.sync_topic_value = topic_value
        self.__sync_event.set()

        if self.__user_callback:
            self.__user_callback(self.sync_topic_value)

