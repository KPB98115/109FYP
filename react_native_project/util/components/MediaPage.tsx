import React, { useState, useContext, useEffect } from 'react';
import { View, Button, StyleSheet, Platform, Text, Image, TouchableOpacity, Modal } from 'react-native';
import { PERMISSIONS, RESULTS, request } from 'react-native-permissions';
import AuthContext from '../data/Context';

type MainPageProps = {
  navigation: any;
}

type InitialPreviewProps = {
  title: string;
  url: string;
}

const API_URL = 'http://120.126.18.145:5000'; //'http://172.31.114.168:5000';

const MediaPage: React.FC<MainPageProps> = ({ navigation }) => {
  const [isMenuShow, setIsMenuShow] = useState(true);
  const [isUploadPageShow, setIsUploadPageShow] = useState(false);
  const [isModalAppear, setIsModalAppear] = useState(false);
  const [initialPreview, setInitialPreview] = useState<InitialPreviewProps[]>([]);
  const authContext = useContext(AuthContext);

  const handleMenuShow = () => {
    setIsMenuShow(!isMenuShow);
  };

  const handleLogOut = () => {
    navigation.navigate('Login');
  };

  const showCollapseIcon = (): string => {
    if (isMenuShow) {
      return '▲';
    }
    return '▼';
  };

  const handleInitialRender = async () => {
    setIsModalAppear(true);
    await fetch(`${API_URL}/get_previewImage`, {
      method: 'GET',
    })
    .then(res => res.json())
    .then(data => {
      // Return all video titles from the server, each item contain video title without extension
      const previewImages: InitialPreviewProps[] = [];
      for (var filename in data) {
        console.log(data[filename]);
        previewImages.push({title: filename, url: `${API_URL}/${data[filename]}`});
      }
      setInitialPreview(previewImages);
    })
    .catch(err => console.error('initiate preview: ', err));
    setIsModalAppear(false);
  };

  const handleRedirectToMediaPlayer = (title: string) => {
    title = title.slice(0, -4);
    if (authContext.selectedURL !== title) {
      if (authContext.isRestricted) {
        authContext.selectedURL = `${API_URL}/static/pixelate_videos/${title}.mp4`;
        //authContext.selectedURL = `${API_URL}/static/pixelate_videos/output_mosaic.mp4`;
      } else {
        authContext.selectedURL = `${API_URL}/static/videos/${title}.mp4`;
      }
      console.log(authContext.selectedURL);
      navigation.navigate('MediaPlayer');
    } else {
      console.log('useContext prop: '+authContext.selectedURL, 'func param: '+title);
    }
  };

  const handlePermissionRequest = async () => {
    let permission;
    if (Platform.OS === 'ios') {
      permission = PERMISSIONS.IOS.PHOTO_LIBRARY;
    } else {
      permission = PERMISSIONS.ANDROID.WRITE_EXTERNAL_STORAGE;
    }
    try {
      const result = await request(permission);
      switch (result) {
        case RESULTS.GRANTED:
          console.log('Permission granted');
          break;
        case RESULTS.DENIED:
          console.log('Permission denied');
          break;
        case RESULTS.BLOCKED:
          console.log('Permission blocked');
          break;
      }
    } catch (e) { console.log(e); }
  };

  const handleUploadAppear = () => {
    navigation.navigate('MediaUpload');
    if (!isUploadPageShow) {
      setIsUploadPageShow(true);
    }
  };

  useEffect(() => {
    handlePermissionRequest();
    handleInitialRender();
  }, []);

  return (
    <>
      <Button title={ showCollapseIcon() } onPress={ handleMenuShow } />
      {isMenuShow && (<View>
        <Button title="上傳" onPress={ handleUploadAppear } />
        <Button title="登出" onPress={ handleLogOut } />
        <Button title="重新整理" onPress={ handleInitialRender } />
      </View>)}
      <View style={ styles.container }>{
        !isModalAppear &&
        <View style={styles.gallery_container}>
          {(initialPreview.map((props: InitialPreviewProps) =>
            <View key={props.title} style={styles.previewImage_container}>
              <TouchableOpacity style={styles.button} onPress={ () => handleRedirectToMediaPlayer(props.title) }>
                <Image
                  style={styles.previewImage}
                  source={{uri: props.url}}
                  alt={ props.title } />
              </TouchableOpacity>
              <Text style={styles.preview_title}>{ props.title }</Text>
            </View>
          ))}
        </View>
        }</View>
      <View style={styles.centeredView}>
        <Modal visible={isModalAppear} animationType="slide" transparent={true}>
          <View style={styles.centeredView}>
            <View style={styles.modalView}>
              <Text style={styles.modalText}>影片資源下載中...</Text>
            </View>
          </View>
        </Modal>
      </View>
    </>
  );
};

var styles = StyleSheet.create({
  navigationBar_container: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignContent: 'center',
  },
  button: {
    width: 100,
    height: 100,
    alignSelf: 'center',
    justifyContent: 'center',
  },
  gallery_container: {
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'flex-start',
    padding: 20,
    //backgroundColor: 'lightgreen',
  },
  previewImage_container: {
    flex: 1,
    width: '33.33%',
    padding: 10,
    justifyContent: 'center',
    //backgroundColor: 'lightblue',
  },
  previewImage: {
    width: '100%',
    height: '100%',
  },
  preview_title: {
    fontSize: 12,
    alignSelf: 'center',
  },
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22,
  },
  modalView: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalText: {
    marginBottom: 15,
    textAlign: 'center',
  },
});

export default MediaPage;
