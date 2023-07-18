import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Authentication from './util/components/Authentication';
import MainPage from './util/components/MainPage';
import { ContextProvider } from './util/data/Context';

const Stack = createNativeStackNavigator();

const App: React.FC = () => {
  return (
    <ContextProvider>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{headerShown: false, animation: 'none'}}>
          <Stack.Screen name="Login" component={Authentication} />
          <Stack.Screen name="MainPage" component={MainPage} />
        </Stack.Navigator>
      </NavigationContainer>
    </ContextProvider>
  );
};

export default App;
