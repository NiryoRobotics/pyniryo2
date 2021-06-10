from threading import Event
import roslibpy


class Topic(object):

    def __init__(self, client, topic_name, topic_type, ):
        self.topic_name = topic_name
        self.topic_type = topic_type
        self.topic = roslibpy.Topic(client, self.topic_name, self.topic_type)

        self.user_callback = None

        self.sync_topic_value = None
        self.sync_event = Event()
        self.sync_event.clear()

    def __call__(self):
        if self.topic.is_subscribed:
            return self.sync_topic_value

        self.subscribe(self.__internal_callback)
        self.sync_event.wait()  # Mettre un timeout au KAZOU
        self.unsubscribe()
        self.sync_event.clear()
        return self.sync_topic_value

    def subscribe(self, callback=None):
        if self.topic.is_subscribed:
            self.topic.subscribe(self.__internal_callback)
            return True
        if callback:
            self.user_callback = callback
        return False

    def unsubscribe(self):
        if self.topic.is_subscribed:
            self.topic.unsubscribe()

    def __internal_callback(self, topic_value):
        self.sync_topic_value = topic_value
        self.sync_event.set()

        if self.user_callback:
            self.user_callback(self.sync_topic_value)
