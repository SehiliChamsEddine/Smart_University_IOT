const mqtt = require("mqtt");

const mqtt_client = mqtt.connect("mqtt://127.0.0.1:1883");
mqtt_client.on("connect", () => {
  console.log("Connected to MQTT broker");

  mqtt_client.publish(
    "sending_control",
    JSON.stringify({ water_pump_status: true }),
    (err) => {
      if (err) {
        console.error("Publish failed:", err);
        mqtt_client.end();
      } else {
        console.log("Message published");
        mqtt_client.end();
        console.log("Disconnected from MQTT broker");
      }
    }
  );
});
