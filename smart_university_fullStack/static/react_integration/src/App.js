import React, { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import SendIcon from "@mui/icons-material/Send";
import { SwitchTextTrack } from "./Customswitch.js";
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);

  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
}
function App() {
  const [sendingData, setSendingData] = useState({
    water_pump_status: false,
    block1_status: false,
    block2_status: false,
    block3_status: false,
  });

  const [receivingData, setReceivingData] = useState({
    water_pump_status: false,
    block1_status: false,
    block2_status: false,
    block3_status: false,
    fire_detection: false,
    gas_detection: false,
  });

  useEffect(() => {
    // Fetch initial values from ControlSettings1
    const fetchInitialValues = async () => {
      try {
        const response = await fetch("/api/control-settings/");
        const data = await response.json();
        setReceivingData(data);
        setSendingData(data);
      } catch (error) {
        console.error("Error fetching initial values:", error);
      }
    };
    fetchInitialValues();

    // Polling to fetch updated values from ControlSettings1 every 2 seconds
    setInterval(async () => {
      try {
        const response = await fetch("/api/control-settings/");
        const data = await response.json();
        setReceivingData(data);
      } catch (error) {
        console.error("Error fetching updated values:", error);
      }
    }, 2000);
  }, []);

  const handleSendData = async () => {
    try {
      const csrftoken = getCookie("csrftoken");
      console.log(csrftoken);
      await fetch("/api/control-settings/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(sendingData),
      });
      console.log("Data sent successfully");
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };

  const handleToggleStatus = (key) => {
    setSendingData((prevData) => ({
      ...prevData,
      [key]: !prevData[key],
    }));
  };

  return (
    <div className="container">
      <h1>Control Settings</h1>
      <div className="chart">
        <h2>Receiving Data</h2>
        <div className="receiving-data  control-settings">
          <p className={receivingData.fire_detection ? "on" : "off"}>
            <p>Fire Detection</p>
            <SwitchTextTrack checked={receivingData.fire_detection} />
          </p>
          <p className={receivingData.gas_detection ? "on" : "off"}>
            <p>Gas Detection</p>
            <SwitchTextTrack checked={receivingData.gas_detection} />
          </p>
          <p className={receivingData.water_pump_status ? "on" : "off"}>
            <p>Water Pump</p>
            <SwitchTextTrack checked={receivingData.water_pump_status} />
          </p>
          <p className={receivingData.block1_status ? "on" : "off"}>
            <p>Block 1</p>
            <SwitchTextTrack checked={receivingData.block1_status} />
          </p>
          <p className={receivingData.block2_status ? "on" : "off"}>
            <p>Block 2</p>
            <SwitchTextTrack checked={receivingData.block2_status} />
          </p>
          <p className={receivingData.block3_status ? "on" : "off"}>
            <p>Block 3</p>
            <SwitchTextTrack checked={receivingData.block3_status} />
          </p>
        </div>
      </div>
      <div className="sending-data chart">
        <h2>Sending Data</h2>
        <div className="control-settings ">
          <button
            className={sendingData.water_pump_status ? "on" : "off"}
            onClick={() => handleToggleStatus("water_pump_status")}
          >
            <p>Water Pump</p>
            <SwitchTextTrack checked={sendingData.water_pump_status} />
          </button>

          <button
            className={sendingData.block1_status ? "on" : "off"}
            onClick={() => handleToggleStatus("block1_status")}
          >
            <p>Block 1</p>
            <SwitchTextTrack checked={sendingData.block1_status} />
          </button>

          <button
            className={sendingData.block2_status ? "on" : "off"}
            onClick={() => handleToggleStatus("block2_status")}
          >
            <p>Block 2</p>
            <SwitchTextTrack checked={sendingData.block2_status} />
          </button>

          <button
            className={sendingData.block3_status ? "on" : "off"}
            onClick={() => handleToggleStatus("block3_status")}
          >
            <p>Block 3 </p>
            <SwitchTextTrack checked={sendingData.block3_status} />
          </button>
        </div>
        <div className="Send">
          <span className="Send-container">
            <Button
              variant="contained"
              endIcon={<SendIcon />}
              onClick={handleSendData}
              sx={{
                backgroundColor: "#299b63",
                "&:hover": {
                  backgroundColor: "#208053", // Change the hover color if needed
                },
              }}
            >
              Send
            </Button>
          </span>
        </div>
      </div>
    </div>
  );
}

export default App;
