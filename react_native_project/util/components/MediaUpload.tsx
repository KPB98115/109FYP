import React, { useState } from 'react';
import { Text, Button, View, StyleSheet } from 'react-native';
import ImageCropPicker from 'react-native-image-crop-picker';
import Video from 'react-native-video';
import CustomModal from './CustomModal';

type MediaUploadProps = {
  navigation: any;
}

type fileInfoProps = {
  path: string;
  name: string;
  type: string;
}

const API_URL = 'http://120.126.18.145:5000'; //'http://172.31.114.168:5000';

const MediaUpload: React.FC<MediaUploadProps> = ({ navigation }) => {
  const [fileInfo, setFileInfo] = useState<fileInfoProps>({
    path: '',
    name: '',
    type: '',
  });

  const [isMediaSelected, setIsMediaSelected] = useState(false);
  const [isMediaUploading, setIsMediaUploading] = useState(false);
  const [isMediaUploaded, setIsMediaUploaded] = useState(false);
  const [mediaFileName, setMediaFileName] = useState('');

  const handleMediaPicker = async () => {
    const video = await ImageCropPicker.openPicker({
      mediaType: 'video',
    })
    .catch(err => console.log(err));
    if (video) {
      console.log(video.filename);
      setFileInfo({
        path: video.path,
        name: video.filename ? video.filename + '.mp4' : Date.now().toString() + '.mp4',
        type: video.mime,
      });
      setMediaFileName(video.filename ? video.filename : Date.now().toString());
      setIsMediaSelected(true);
    }
  };

  const handleNavigateBack = () => {
    setFileInfo({ path: '', name: '', type: '' });
    setIsMediaUploading(false);
    setIsMediaUploaded(false);
    setIsMediaSelected(false);
    navigation.navigate('MediaPage');
  };

  const handleFileUpload = async () => {
    setIsMediaUploading(true);
    let formData = new FormData();
    formData.append('file', {
      uri: fileInfo.path,
      type: fileInfo.type,
      name: fileInfo.name,
    } as unknown as Blob); // Cast object to Blob

    fetch(`${API_URL}/video_pixelation`, {
      method: 'POST',
      headers: { 'Content-Type': 'multipart/form-data' },
      body: formData,
    })
    .then(res => {
      console.log(res.status);
      setIsMediaUploaded(true);
      setIsMediaUploading(false);
    })
    .catch(error => console.error(error));
  };

  const handleFinishUpload = () => {
    setIsMediaSelected(false);
    setIsMediaUploaded(false);
    ImageCropPicker.clean()
    .then(() => {
      setFileInfo({path: '', name: '', type: ''});
      console.log('Clean up all temporary files from temp dictionary.');
    })
    .catch(e => console.log(e));
  };

  return (<View style={styles.container}>
    <Button title="返回" onPress={ handleNavigateBack } />
    <Button title="選擇影片" onPress={ handleMediaPicker } />
    {isMediaSelected && <>
      <Text>已選擇影片: {mediaFileName}</Text>
      <View style={styles.mediaPlayerContainer}>
        <Video
            source={{ uri: fileInfo.path }}
            style={ styles.mediaPlayer }
            controls={false}
            paused={false}
            resizeMode="contain" />
      </View>
      <Button title="上傳" onPress={ handleFileUpload } />
    </>}
    { isMediaUploading && <CustomModal modalText={'正在上傳...'} modalCallback={()=>{}} isButtonAppear={false} /> }
    { isMediaUploaded && <CustomModal modalText={'影片上傳成功'} modalCallback={ handleFinishUpload } isButtonAppear={true} /> }
  </View>);
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
    alignContent: 'center',
  },
  mediaPlayerContainer: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
  },
  mediaPlayer: {
    alignSelf: 'center',
    width: '100%',
    height: '100%',
  },
});

export default MediaUpload;
