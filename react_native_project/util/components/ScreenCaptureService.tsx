import React, { useContext, useEffect, useRef } from 'react';
import { View, StyleSheet } from 'react-native';
import ViewShot from 'react-native-view-shot';
import { captureScreen } from 'react-native-view-shot';
import BackgroundTimer from 'react-native-background-timer';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import RNFS from 'react-native-fs';
import AuthContext from '../data/Context';

const ScreenCaptureService: React.FC = () => {
  console.log('Start captureing...');
  const camera = useRef<Camera>(null);
  const authContext = useContext(AuthContext);
  const devices = useCameraDevices();
  const device: any = devices.front;
  const captureInterval = 1000;

  const facialCapture = async () => {
    if (camera.current !== null) {
      const snapshot = await camera.current.takeSnapshot({
        quality: 100,
      });
      console.log(snapshot.path);
      const formData = new FormData();
      formData.append('username', authContext.currentUser);
      if (snapshot.path === '') {
        return;
      }
      await RNFS.readFile(snapshot.path, 'base64').then(base64_image => {
        formData.append('image', base64_image);
      });
      fetch('http://172.31.114.168:5000/realtime_authenticate', {
        method: 'POST',
        headers: {'Content-Type': 'multipart/form-data'},
        body: formData,
      }).then(res => res.json()).then(json => {
        if (json.auth) {
          console.log(json.status);
        }
        else {
          console.error(json.status);
        }
      }).catch(error => console.log(error));
    }
  };

  const screenCapture = async () => {
    captureScreen({ format: 'jpg', quality: 1, result: 'base64' }).then(async (base64_image) => {
      const formData = new FormData();
      formData.append('image', base64_image);

      fetch('http://172.31.114.168:5000/screen_detection', {
        method: 'POST',
        headers: {'Content-Type': 'multipart/form-data'},
        body: formData,
      }).then(res => res.json()).then(result => console.log(result)).catch((error) => {
        console.error('Error uploading screenshot:', error);
      });
    });
  };

  // Get the device permission to access camera
  useEffect(() => {
    async function getPermission() {
      const newCameraPermission = await Camera.requestCameraPermission();
      console.log(newCameraPermission);
    }
    getPermission();
  }, []);

  useEffect(() => {
    const captureScreenInterval = BackgroundTimer.setInterval(() => {
      facialCapture();
      screenCapture();
    }, captureInterval);

    return () => {
      console.log('Stop captureing...');
      BackgroundTimer.clearInterval(captureScreenInterval);
    };
  }, [captureInterval]);

  if (device == null) { return null; }

  return (
    <>
      <ViewShot />
      <View style={styles.cameraContainer}>
        <Camera
          ref={camera}
          style={StyleSheet.absoluteFill}
          device={device}
          isActive={true}
          photo={true}
        />
      </View>
    </>
    );
};

const styles = StyleSheet.create({
  cameraContainer: {
    // Set Camera Component to off screen position
    position: 'absolute',
    bottom: -1000,
  },
});

export default ScreenCaptureService;
