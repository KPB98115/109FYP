import React from 'react';
import { Button, Image, Text } from 'react-native';

type VideoPreviewImageProps = {
  image: string;
  isRendered: boolean;
  title: string;
  passParamToParent: (title: string) => void;
}

const PreviewImage: React.FC<VideoPreviewImageProps> = ({ title, image, isRendered, passParamToParent }) => {

  return (<>
    { console.log('Flag') }
    <Text>{ title }</Text>
    <Image source={{uri: image}} />
    <Button title="Play" onPress={() => passParamToParent(title)} />
  </>);
};

export default PreviewImage;
