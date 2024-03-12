import React, { useContext, useEffect, useRef, useState } from 'react';
import { View, StyleSheet } from 'react-native';
import BackgroundTimer from 'react-native-background-timer';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import RNFS from 'react-native-fs';
import AuthContext from '../data/Context';
import { accelerometer } from 'react-native-sensors';

type ScreenCaptureServiceProps = {
  isAuthFail: (isFail: boolean, failCount: number) => void;
  forceToLogout: () => void;
}

let lastTimestamp = Date.now();
let lastX = 0;
let lastY = 0;
let lastZ = 0;
const threshold = 1.00; // Threshold for motion detection
const API_URL = 'http://120.126.18.145:5000'; //'http://172.31.114.168:5000';

const ScreenCaptureService: React.FC<ScreenCaptureServiceProps> = ({ isAuthFail, forceToLogout }) => {
  const camera = useRef<Camera>(null);
  const authContext = useContext(AuthContext);
  const devices = useCameraDevices();
  const device: any = devices.front;
  const captureInterval = 1000;
  //const [isLogin, setIslogin] = useState(true);
  const [isMotionDetected, setIsMotionDetected] = useState(false);
  const [failToAuthCount, setFailToAuthCount] = useState(0);
  const controller = new AbortController();
  const signal = controller.signal;

  const facialCapture = async () => {
    if (camera.current !== null) {
      const snapshot = await camera.current.takeSnapshot({
        quality: 100,
      });
      const formData = new FormData();
      formData.append('username', authContext.currentUser);
      if (snapshot.path !== '') {
        await RNFS.readFile(snapshot.path, 'base64').then(base64_image => {
          formData.append('image', base64_image);
        });
      } else {
        return;
      }
      fetch(`${API_URL}/realtime_authentication`, {
        method: 'POST',
        headers: {'Content-Type': 'multipart/form-data'},
        body: formData,
        signal: signal,
      })
      .then(res => res.json())
      .then(data => {
        console.log('auth: ', data.auth, 'status: ', data.status);
        // For testing
        if (authContext.currentUser === 'root') {
          return;
        }
        if (!data.auth) {
          console.log('unauthorized user detected.');
          setFailToAuthCount(prev => prev + 1);
          isAuthFail(true, failToAuthCount);
          return;
        } else {
          setFailToAuthCount(0);
          isAuthFail(false, failToAuthCount);
          return;
        }
      })
      .catch(error => console.log(error));
      // Delete the image to release device memory
      RNFS.unlink(snapshot.path)
      .then(() => {
        console.log('Image deleted successfully.');
      });
    }
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
    if (failToAuthCount < 3) {
      if (failToAuthCount === 0) {
        isAuthFail(false, failToAuthCount);
      } else {
        isAuthFail(true, failToAuthCount);
      }
    } else {
      forceToLogout();
      console.log('Access declined: Unauthorized user detected.');
    }
  }, [failToAuthCount]);

  useEffect(() => {
    if (!authContext.isLoggedIn) {
      controller.abort();
    }
  }, [authContext.isLoggedIn]);

  useEffect(() => {
    const captureScreenInterval = BackgroundTimer.setInterval(() => {
      if (!isMotionDetected) {
        facialCapture();
      }
    }, captureInterval);

    return () => {
      BackgroundTimer.clearInterval(captureScreenInterval);
    };
  }, [captureInterval]);

  // Implement the motion detection to improve performance of every frame
  useEffect(() => {
    const accelerometerSubscription = accelerometer.subscribe(({ x, y, z, timestamp }) => {
      const timeDelta = timestamp - lastTimestamp;
      const xDelta = Math.abs(x - lastX);
      const yDelta = Math.abs(y - lastY);
      const zDelta = Math.abs(z - lastZ);

      if (xDelta > threshold || yDelta > threshold || zDelta > threshold || timeDelta > lastTimestamp) {
        setIsMotionDetected(true);
      }
      else {
        setIsMotionDetected(false);
      }

      lastTimestamp = timestamp;
      lastX = x;
      lastY = y;
      lastZ = z;
    });

    return () => {
      if (accelerometerSubscription) {
        accelerometerSubscription.unsubscribe();
      }
    };
  }, []);

  if (device == null) { return null; }

  return (
    <View style={styles.cameraContainer}>
      <Camera
        ref={camera}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true} />
    </View>
  );
};

const styles = StyleSheet.create({
  cameraContainer: {
    // Set Camera Component to off screen position
    position: 'absolute',
    bottom: -1000,
    width: '100%',
    height: '100%',
  },
});

export default ScreenCaptureService;
