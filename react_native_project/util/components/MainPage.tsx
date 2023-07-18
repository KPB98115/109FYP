import React, { useState, useRef, useCallback } from 'react';
import { View, Button, StyleSheet, TextInput, TouchableOpacity, Text } from 'react-native';
import { WebView, WebViewNavigation } from 'react-native-webview';
import ScreenCaptureService from './ScreenCaptureService';
import { NativeModules } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';

interface MainPageProps {
  navigation: any;
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

  const startCapture = () => {
    console.error('Start capturing');
    setIsCapturing(true);
  };

  const stopCapture = () => {
    console.error('Stop capturing');
    setIsCapturing(false);
  };

  const handleMenuShow = () => {
    setIsMenuShow(!isMenuShow);
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
    const removeAllPixelate = `
    var pixelateBox = document.getElementByClassName('pixelateBox');
      if (pixelateBox) {
        pixelateBox.remove();
      }
    `;
    webViewRef.current?.injectJavaScript(removeAllPixelate);
    setUrl(input);
  };

  const handleNavigated = (navState: WebViewNavigation) => {
    setInput(navState.url);
  };

  const clearTextOnFocus = () => {
    setPreviousNavigatedUrl(url);
    setInput('');
  };

  useFocusEffect(
    useCallback(() => {
      // Do something when the screen is focused
      console.log('MainPage component is focused');
      //setIsWebViewLoaded(true);

      return () => {
        // Do something when the screen is unfocused
        console.log('MainPage component is blurred');
        //setIsWebViewLoaded(false);
        // Useful for cleanup functions
      };
    }, [])
  );

  const appendPixelatedDiv = (pA: number[], pC: number[]) => {
    // The parameters is the top left and bottom right coordinate of the pixelated content
    const width = Math.abs(pA[0] - pC[0]) + 'px';
    const height = Math.abs(pA[1] - pC[1]) + 'px';
    const top = Math.min(pA[1], pC[1]) + 'px';
    const left = Math.min(pA[0], pC[0]) + 'px';
    const divID = pA[0] * pA[1] * pC[0] * pC[1];

    console.log(pA, pC);

    const script = `
      var pixelDiv = document.createElement('div');
      pixelDiv.id = ${divID}
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

  const randomNum = (): number => {
    return Math.floor(Math.random() * 500);
  };

  return (
    <>
      {isCapturing && (
        <ScreenCaptureService />
      )}
      <Button title={showCollapseIcon()} onPress={handleMenuShow} />
      {isMenuShow && (<View>
        <Button title='Native Screenshot' onPress={handleNativeCapture} />
        <Button title="Start Capture" onPress={startCapture} />
        <Button title="Stop Capture" onPress={stopCapture} />
        <Button title="Logout" onPress={() => {
          stopCapture();
          navigation.navigate('Login');
        }} />
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
        <Button title="pixelate" onPress={() => appendPixelatedDiv([randomNum(), randomNum()], [randomNum(), randomNum()])} />
      </View>
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
