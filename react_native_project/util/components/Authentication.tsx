import React, { useContext, useState, useRef, useEffect } from 'react';
import { Button, Text, TextInput, Image, useWindowDimensions, StyleSheet, View } from 'react-native';
import { Camera, useCameraDevices } from 'react-native-vision-camera';
import { TabView, SceneMap } from 'react-native-tab-view';
import AuthContext from '../data/Context';
import RNFS from 'react-native-fs';

interface AuthenticationProps {
  navigation: any;
}

const Authentication:React.FC<AuthenticationProps> = ({ navigation }) => {
  const [index, setIndex] = useState(0);
  const [routes] = React.useState([
    { key: 'first', title: '使用帳號密碼登入' },
    { key: 'second', title: '使用臉部辨識登入' },
  ]);
  const [isCaptured, setIsCaptured] = useState(false);
  const [snapshotURL, setSnapshotURL] = useState('');

  const camera = useRef<Camera>(null);
  const devices = useCameraDevices();
  const device: any = devices.front;

  const authContext = useContext(AuthContext);

  let username: string = '';
  let password: string = '';

  const layout = useWindowDimensions();

  const setUsername = (name: string) => { username = name; };
  const setPassword = (pw: string) => { password = pw; };

  // Get the device permission to access camera
  useEffect(() => {
    async function getPermission() {
      await Camera.requestCameraPermission();
    }
    getPermission();
  }, []);

  useEffect(() => {
    const unSubscribed = navigation.addListener('blur', () => {
      // Do something when user left Authentication component
      console.log('Authentication component is blurred');
    });

    return unSubscribed;
  }, [navigation]);

  const handleCapture = async () => {
    if (camera.current !== null) {
      // Take a snapshot for image preview
      const snapshot = await camera.current.takeSnapshot({
        quality: 80,
      });
      setSnapshotURL(snapshot.path);
      setIsCaptured(true);
      console.log(snapshot.path);
    }
    else {
      console.error('Camera not intialized');
    }
  };

  const handleSimpleLogin = async () => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    await fetch('http://172.20.10.4:5000/authentication', {
      method: 'POST',
      headers: {'Content-Type': 'multipart/form-data'},
      body: formData,
    }).then(res => res.json()).then(json => {
      authContext.isLoggedIn = true;
      authContext.currentUser = json.user;
      navigation.navigate('MainPage');
    }).catch((error) => {
      console.error('Error: failed login:', error);
    });
  };

  const handleFaicalLogin = async () => {
    const formData = new FormData();
    if (snapshotURL === '') {
      return;
    }
    await RNFS.readFile(snapshotURL, 'base64').then(base64_image => {
      console.log(base64_image.slice(0,20));
      formData.append('image', base64_image);
    });
    // Access the image file in device storage via url
    //Platform.OS === 'android' ? uri : setUri(uri.replace('file://', ''));
    //fetch(uri).then(res => res.blob()).then(blob => formData.append('image', blob, 'login_user.jpg'));
    await fetch('http://172.31.114.168:5000/facial_authentication', {
      method: 'POST',
      headers: {'Content-Type': 'multipart/form-data'},
      body: formData,
    }).then(res => res.json()).then(json => {
      if (json.auth) {
        authContext.isLoggedIn = true;
        authContext.currentUser = json.user;
        navigation.navigate('MainPage');
        console.log(`Logged-in user: ${authContext.currentUser}`);
      }
      else {
        console.error('Login unsucessful');
      }
    }).catch((error) => {
      console.error('Error: failed login:', error);
    });
  };

  return (
    <>
      <TabView
        navigationState={{ index, routes }}
        renderScene={SceneMap({
          first: () => (
            <>
              <TextInput
                placeholder="Username"
                //value={username}
                onChangeText={setUsername} />
              <TextInput
                placeholder="Password"
                //value={password}
                onChangeText={setPassword} />
              <Button title="登入" onPress={ handleSimpleLogin } />
            </>),
          second: () => (
            <>
              {isCaptured ?
                (<>
                  <View style={styles.container}><Image source={{uri:`file://${snapshotURL}`}} style={styles.image}/></View>
                  <Button title="登入" onPress={ handleFaicalLogin } />
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
                  <Button title="截圖" onPress={ handleCapture } />
                </>)}
            </>
          ),
        })}
        onIndexChange={ setIndex } // Pass in the index to change index state: setIndex(index)
        initialLayout={{ width: layout.width }} />
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
});

export default Authentication;
