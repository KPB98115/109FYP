import React, { useState } from 'react';
import { Button } from 'react-native';
import ScreenCaptureService from './ScreenCaptureService';

interface MainPageProps {
  navigation: any;
}

const MainPage: React.FC<MainPageProps> = ({ navigation }) => {
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
        <ScreenCaptureService />
      )}
      <Button title="Start Capture" onPress={startCapture} />
      <Button title="Stop Capture" onPress={stopCapture} />
      <Button title="Logout" onPress={() => navigation.goBack()} />
    </>
  );
};

export default MainPage;
