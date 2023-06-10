import React, { useEffect, useRef } from 'react';
import { captureScreen } from 'react-native-view-shot';
import ViewShot from 'react-native-view-shot';
import BackgroundTimer from 'react-native-background-timer';

interface ScreenCaptureServiceProps {
  captureInterval: number;
  apiUrl: string;
}

const ScreenCaptureService: React.FC<ScreenCaptureServiceProps> = ({ captureInterval, apiUrl }) => {
  const captureRef = useRef<ViewShot>(null);

  useEffect(() => {
    const captureScreenInterval = BackgroundTimer.setInterval(() => {
      captureScreen({ format: 'png', quality: 1, result: 'data-uri' }).then((uri: string) => {
        const imageData = uri.split(',')[1];
        const imageName = `screenshot_${Date.now()}.png`;

        fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'image/png',
            'Content-Disposition': `attachment; filename="${imageName}"`,
          },
          body: imageData,
        })
          .then((response) => response.json())
          .then((responseData) => {
            console.log(responseData);
            // It return a list of items as json object
          })
          .catch((error) => {
            console.error('Error uploading screenshot:', error);
          });
      });
    }, captureInterval);

    return () => {
      BackgroundTimer.clearInterval(captureScreenInterval);
    };
  }, [captureInterval, apiUrl]);

  return <ViewShot ref={captureRef} />;
};

export default ScreenCaptureService;
