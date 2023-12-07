import React, { useContext } from 'react';
import { Button, TextInput } from 'react-native';
import AuthContext from '../data/Context';

type AuthenticationProps = {
  navigation: any;
}

const API_URL = 'http://120.126.18.145:5000'; //'http://172.31.114.168:5000';

const SimpleLogin: React.FC<AuthenticationProps> = ({ navigation }) => {
  let username: string = '';
  let password: string = '';

  const authContext = useContext(AuthContext);

  const setUsername = (name: string) => { username = name; };
  const setPassword = (pw: string) => { password = pw; };

  const handleSimpleLogin = async () => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    await fetch(`${API_URL}/authentication`, {
      method: 'POST',
      headers: {'Content-Type': 'multipart/form-data'},
      body: formData,
    }).then(res => res.json()).then(json => {
      authContext.isLoggedIn = true;
      authContext.currentUser = json.user;
      navigation.navigate('MediaPage');
    }).catch((error) => {
      console.error('Error: failed login:', error);
    });
  };

  const testLogin = () => {
    authContext.isLoggedIn = true;
    authContext.currentUser = 'Kingston';
    navigation.navigate('MediaPage');
  };

  return (
    <>
      <Button title="新用戶註冊" onPress={ () => navigation.navigate('Registration') } />
      <TextInput
        placeholder="使用者名稱"
        //value={username}
        onChangeText={setUsername} />
      <TextInput
        placeholder="使用者密碼"
        //value={password}
        onChangeText={setPassword} />
      <Button title="登入" onPress={ testLogin } />
    </>
  );
};

export default SimpleLogin;
