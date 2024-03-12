import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Authentication from './util/components/Authentication';
//import MainPage from './util/components/MainPage';
import MediaPage from './util/components/MediaPage';
import MediaUpload from './util/components/MediaUpload';
import MediaPlayer from './util/components/MediaPlayer';
import { ContextProvider } from './util/data/Context';
import Registration from './util/components/Registration';

const Stack = createNativeStackNavigator();

const App: React.FC = () => {
  return (
    <ContextProvider>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{headerShown: false, animation: 'none'}}>
          <Stack.Screen name="Login" component={ Authentication } />
          <Stack.Screen name="MediaPage" component={ MediaPage } />
          <Stack.Screen name="MediaUpload" component={ MediaUpload } />
          <Stack.Screen name="MediaPlayer" component={ MediaPlayer } />
          <Stack.Screen name="Registration" component={ Registration } />
        </Stack.Navigator>
      </NavigationContainer>
    </ContextProvider>
  );
};

export default App;
