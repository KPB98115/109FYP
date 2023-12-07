import React, { useState, useContext } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import Video from 'react-native-video';
import ScreenCaptureService from './ScreenCaptureService';
import AuthContext from '../data/Context';

type MediaPlayerProps = {
  navigation: any;
}

const MediaPlayer: React.FC<MediaPlayerProps> = ({ navigation }) => {
  const authContext = useContext(AuthContext);
  const [isBlackScreen, setIsBlackScreen] = useState(false);
  const [failToAuthCount, setFailToAuthCount] = useState(0);

  const handleBlackScreen = (isAuthFailed: boolean, count: number) => {
    if (isAuthFailed) {
      console.log('block the screen');
    }
    setFailToAuthCount(count);
    setIsBlackScreen(isAuthFailed);
  };

  const handleRedirect = () => {
    navigation.navigate('MediaPage');
  };

  const handleLogOut = () => {
    authContext.isLoggedIn = false;
    authContext.selectedURL = '';
    authContext.currentUser = '';
    navigation.navigate('Login');
    console.log(authContext);
  };

  return (<View style={ Styles.container }>
    <View style={ isBlackScreen ? Styles.blackScreen : Styles.container }>
      <Text style={{color: !isBlackScreen ? 'green' : 'red', fontSize: 24, textAlign: 'center'}}>認證狀態：{ !isBlackScreen ? '授權使用者' : '非授權使用者'}</Text>
      { isBlackScreen && <Text style={{ color: 'white', textAlign: 'center' }}>已認證失敗：{ failToAuthCount }次，累積三次即自動登出</Text> }
      <View style={ Styles.mediaPlayerContainer }>
        <Video
          source={{ uri: authContext.selectedURL }}
          style={isBlackScreen ? Styles.mediaPlayerInBlackScreen : Styles.mediaPlayer }
          controls={true}
          repeat={true}
          paused={true}
          resizeMode="contain" />
      </View>
    </View>
    <Button title="關閉" onPress={ handleRedirect } />
    <ScreenCaptureService isAuthFail={ handleBlackScreen } forceToLogout={ handleLogOut } />
  </View>);
};

const Styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignContent: 'center',
    backgroundColor: 'black',
  },
  mediaPlayerContainer: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
  },
  mediaPlayer: {
    width: '100%',
    height: '37%',
  },
  mediaPlayerInBlackScreen: {
    width: '0%',
    height: '0%',
  },
  blackScreen: {
    flex: 1,
    backgroundColor: 'black',
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default MediaPlayer;
