import React, { useState } from 'react';
import { Button } from 'react-native';
import ScreenCaptureService from './util/components/ScreenCaptureService';

const App: React.FC = () => {
  const [isCapturing, setIsCapturing] = useState(false);

  const startCapture = () => {
    setIsCapturing(true);
  };

  const stopCapture = () => {
    setIsCapturing(false);
  };

  return (
    <>
      {isCapturing && (
        <ScreenCaptureService
          captureInterval={5000} // Capture interval in milliseconds (5 seconds)
          apiUrl="https://your-api-endpoint.com/upload" // Replace with your API endpoint
        />
      )}
      <Button title="Start Capture" onPress={startCapture} />
      <Button title="Stop Capture" onPress={stopCapture} />
    </>
  );
};

export default App;
