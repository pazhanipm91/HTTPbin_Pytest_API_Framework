import allure

class TestRabbitMQIntegration:
    @allure.step("Publishing and consuming a message from RabbitMQ")
    def test_publish_and_consume(self, rabbitmq_channel):
        message = "Hello RabbitMQ"

        with allure.step("Publish a message to the queue"):
            rabbitmq_channel.basic_publish(
                exchange="", routing_key="test_queue", body=message
            )

        with allure.step("Consume the message from the queue"):
            method_frame, header_frame, body = rabbitmq_channel.basic_get(
                queue="test_queue", auto_ack=True
            )

        with allure.step("Verify message correctness"):
            assert body.decode() == message, "Message was not consumed correctly"
