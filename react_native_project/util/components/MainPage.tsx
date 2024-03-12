import React, { useState, useRef, useContext, useEffect } from 'react';
import { View, Button, StyleSheet, TextInput, TouchableOpacity, Text } from 'react-native';
import ScreenCaptureService from './ScreenCaptureService';
import { NativeModules } from 'react-native';
import AuthContext from '../data/Context';

interface MainPageProps {
  navigation: any;
}

interface PixelatedProps {
  topLeft: any[];
  bottomRight: any[];
}

interface ForbiddenCoordinates {
  name: string;
  xmin: number;
  ymin: number;
  xmax: number;
  ymax: number;
}

const { NativeScreenshotModule } = NativeModules;

const MainPage: React.FC<MainPageProps> = ({ navigation }) => {
  const webViewRef = useRef<WebView>(null);
  const [isMenuShow, setIsMenuShow] = useState(true);
  const [isCapturing, setIsCapturing] = useState(false);
  const [url, setUrl] = useState('https://www.google.com/');
  const [input, setInput] = useState(url);
  const [previousNavigatedUrl, setPreviousNavigatedUrl] = useState(url);
  const [isWebViewLoaded, setIsWebViewLoaded] = useState(false);
  const authContext = useContext(AuthContext);
  const [pixelateArea, setPixelateArea] = useState<PixelatedProps>({topLeft: [], bottomRight: []});
  const [detectedItems, setDetectedItems] = useState<String[]>([]);

  const startCapture = () => {
    console.log('startCapturing');
    setIsCapturing(true);
    //setIsMenuShow(!isMenuShow);
  };

  const stopCapture = () => {
    console.log('Stop capturing');
    setIsCapturing(false);
  };

  const handleMenuShow = () => {
    setIsMenuShow(!isMenuShow);
  };

  const handleLoginOut = () => {
    setIsCapturing(false);
    authContext.currentUser = '';
    navigation.navigate('Login');
  };

  const showCollapseIcon = (): string => {
    if (isMenuShow) {
      return '▲';
    }
    return '▼';
  };

  const handleUrlChange = (inputUrl: string) => {
    setInput(inputUrl);
  };

  const handleRedirect = () => {
    removeAllPixelateArea();
    setUrl(input);
  };

  const handleNavigated = (navState: WebViewNavigation) => {
    setInput(navState.url);
  };

  const clearTextOnFocus = () => {
    setPreviousNavigatedUrl(url);
    setInput('');
  };

  /**
   * Called when the repsonse is received from the ScreenCaptureService.tsx component.
   * @param coordinates should be a list of objects containing forbidden objects or areas.
  */
  const handleScreenCaptureResponse = (coordinates: any) => {
    let itemsName: String[] = [];
    coordinates.map((coor: ForbiddenCoordinates) => {
      itemsName.push(coor.name);
      const topLeft: number[] = [coor.xmin, coor.ymin];
      const bottomRight: number[] = [coor.xmax, coor.ymax];
      setPixelateArea({topLeft: topLeft, bottomRight: bottomRight});
    });
    setDetectedItems(itemsName);
  };

  useEffect(() => {
    if (isCapturing) {
      // The re-render may not be triggered if the value remains the same
      console.log('Append the pixelate div on: ', pixelateArea);
      appendPixelatedDiv(pixelateArea.topLeft, pixelateArea.bottomRight);
    }
  },[pixelateArea]);

  /**
   * To append custom div into WebView DOM.
   * @param topLeft should be a list of numbers that represent coordinates
   * @param bottomRight should be a list of numbers that represent coordinates
   */
  const appendPixelatedDiv = (topLeft:number[], bottomRight:number[]) => {
    // The parameters is the top left and bottom right coordinate of the pixelated content
    const width = Math.abs(topLeft[0] - bottomRight[0]) + 'px';
    const height = Math.abs(topLeft[1] - bottomRight[1]) + 'px';
    const top = Math.min(topLeft[1], bottomRight[1]) + 'px';
    const left = Math.min(topLeft[0], bottomRight[0]) + 'px';
    const divID = topLeft[0] * topLeft[1] * bottomRight[0] * bottomRight[1];
    const script = `
      try {
        pixelDiv.remove();
      } catch {
        console.log('pixelDiv does not exist.');
      }
      var pixelDiv = document.createElement('div');
      pixelDiv.id = ${divID}
      pixelDiv.className = 'pixelateBox';
      pixelDiv.innerHTML = 'Pixelated Div';
      pixelDiv.style.position = 'absolute';
      pixelDiv.style.width = '${width}';
      pixelDiv.style.height = '${height}';
      pixelDiv.style.top = '${top}';
      pixelDiv.style.left = '${left}';
      pixelDiv.style.zIndex = '999';
      pixelDiv.style.backgroundColor = '#e0a3ff';
      document.querySelector('body').style.position = 'relative';
      document.querySelector('body').appendChild(pixelDiv);
    `;
    if (isWebViewLoaded) {
      webViewRef.current?.injectJavaScript(script);
    }
  };

  const removeAllPixelateBox = () => {
    const removeAllPixelate = `
      pixelDiv.remove();
    `;
    webViewRef.current?.injectJavaScript(removeAllPixelate);
  };

  useEffect(() => {
    if (authContext.currentUser === '') {
      stopCapture();
      navigation.navigate('Login');
    }
  },[authContext.currentUser]);

  /**
  const handleNativeCapture = async () => {
    const base64_screenshot = await NativeScreenshotModule.captureScreenshot();
    const formData = new FormData();
    formData.append('screenshot', base64_screenshot);
    fetch('http://172.31.114.168:5000/screenshot_detection', {
        method: 'POST',
        headers: {'Content-Type': 'multipart/form-data'},
        body: formData,
      })
      .then(res => res.json())
      .then(result => console.log(result))
      .catch((error) => {
        console.error('Error uploading screenshot:', error);
      });
  };
  */

  return (
    <>
      {isCapturing && (
        <ScreenCaptureService passResponseToMain={handleScreenCaptureResponse} />
      )}
      <Button title={showCollapseIcon()} onPress={handleMenuShow} />
      {isMenuShow && (<View>
        <Button title="Start Capture" onPress={startCapture} />
        <Button title="Stop Capture" onPress={stopCapture} />
        <Button title="Logout" onPress={handleLoginOut} />
      </View>)}
      <View style={{flex: 1, display: isMenuShow ? 'none' : 'flex'}}>
        <View style={styles.navigationBar_container}>
          <Button title='Back' onPress={() => webViewRef.current?.goBack()} />
          <TextInput
            style={styles.inputText}
            value={input}
            onChangeText={handleUrlChange}
            onEndEditing={handleRedirect}
            onBlur={() => input.length ? null : setInput(previousNavigatedUrl)}
            clearTextOnFocus={true}
            autoCapitalize="none"
          />
          <TouchableOpacity style={styles.emtpyInputButton} onPress={clearTextOnFocus}>
            <Text style={{ marginRight: 20 }}> X </Text>
          </TouchableOpacity>
        </View>
        <WebView
          ref={webViewRef}
          source={{ uri: url }}
          onNavigationStateChange={handleNavigated}
          onLoadEnd={() => setIsWebViewLoaded(true)} />
      </View>
      {!isMenuShow && <>
        <Text>Items: {detectedItems}</Text>
        <Button title="clear" onPress={ removeAllPixelateBox } />
      </>}
    </>
  );
};

var styles = StyleSheet.create({
  navigationBar_container: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  emtpyInputButton: {
    justifyContent: 'center',
    borderWidth: 1,
    borderLeftWidth: 0,
  },
  inputText: {
    flex: 1,
    height: 40,
    borderWidth: 1,
    borderRightWidth: 0,
  },
});

export default MainPage;
