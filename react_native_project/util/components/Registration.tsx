import React, { useEffect, useRef, useState } from 'react';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import { Button, View, Text, Image, StyleSheet, TextInput } from 'react-native';
import RNFS from 'react-native-fs';
import { accelerometer } from 'react-native-sensors';
import CustomModal from './CustomModal';

type AuthenticationProps = {
  navigation: any;
}

let lastTimestamp = Date.now();
let lastX = 0;
let lastY = 0;
let lastZ = 0;
const threshold = 0.09; // Threshold for motion detection
const API_URL = 'http://120.126.18.145:5000'; //'http://172.31.114.168:5000';

const Registration: React.FC<AuthenticationProps> = ({ navigation }) => {

  const [isCaptured, setIsCaptured] = useState(false);
  const [snapshotURL, setSnapshotURL] = useState('');
  const [username, onChangeUsername] = useState('');
  const [password, onChangePassword] = useState('');
  const [isRegistedSuccess, setIsRegistedSuccess] = useState(false);
  const [isMotionDetected, setIsMotionDetected] = useState(false);
  const camera = useRef<Camera>(null);
  const devices = useCameraDevices();
  const device: any = devices.front;

  // Get the device permission to access camera
  useEffect(() => {
    async function getPermission() {
      await Camera.requestCameraPermission();
    }
    getPermission();
  }, []);

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

  const handleCapture = async () => {
    if (camera.current !== null) {
      // Take a snapshot for image preview
      const snapshot = await camera.current.takeSnapshot({
        quality: 80,
      });
      setSnapshotURL(snapshot.path);
      setIsCaptured(true);
    }
    else {
      console.error('Camera not intialized');
    }
  };

  const handleRegistration = async () => {
    const formData = new FormData();
    if (snapshotURL !== '') {
      await RNFS.readFile(snapshotURL, 'base64').then(async base64_image => {
        formData.append('image', base64_image);
      });
    } else {
      return;
    }
    if (username && password) {
      formData.append('username', username);
      formData.append('password', password);
    }
    await fetch(`${API_URL}/registration`, {
      method: 'POST',
      headers: {'Content-Type': 'multipart/form-data'},
      body: formData,
    }).then(res => res.json())
    .then(data => {
      console.log(data);
      if (data.result) {
        navigation.navigate('Login');
        setIsCaptured(false);
        setIsRegistedSuccess(true);
        console.warn('使用者註冊成功！');
      }
      else {
        setIsCaptured(false);
        console.error('使用者註冊失敗！');
      }
    });
    // Delete the image to release device memory
    RNFS.unlink(snapshotURL)
    .then(() => {
      console.log('Image deleted successfully.');
    });
  };

  const handleRedirect = () => {
    setIsRegistedSuccess(false);
    navigation.navigate('Login');
  };

  return (
    <>
      <View>
        <TextInput
          style={styles.inputField}
          onChangeText={ onChangeUsername }
          //value={username}
          placeholder="使用者名稱" />
        <TextInput
          style={styles.inputField}
          onChangeText={ onChangePassword }
          //value={password}
          placeholder="使用者密碼" />
      </View>
      {isCaptured ?
        (<>
          <View style={styles.container}><Image source={{uri:`file://${snapshotURL}`}} style={styles.image}/></View>
          <Button title="註冊" onPress={ handleRegistration } />
          <Button title="重拍" onPress={ () => setIsCaptured(false) } />
        </>) :
        (<>
          {device == null ? <Text>Loading...</Text> : <View style={styles.container}>
          <Camera
            ref={camera}
            style={StyleSheet.absoluteFill}
            device={device}
            isActive={true}
            photo={true}
          />
          </View>}
          {isMotionDetected ?
            <Button title="Motion detected" /> :
            <Button title="截圖" onPress={ handleCapture } />}
        </>
      )}
      { isRegistedSuccess && <CustomModal modalText={'註冊成功！\n請重新登入'} isButtonAppear={true} modalCallback={ handleRedirect } />}
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignContent: 'center',
  },
  camButton: {
    alignSelf: 'center',
    justifyContent: 'flex-end',
  },
  image: {
    width: '100%',
    height: '100%',
  },
  inputField: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
});

export default Registration;
