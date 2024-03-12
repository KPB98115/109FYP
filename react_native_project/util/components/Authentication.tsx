import React, { useState } from 'react';
import { useWindowDimensions, Button } from 'react-native';
import { TabView, SceneMap } from 'react-native-tab-view';
import SimpleLogin from './SimpleLogin';
import FacialLogin from './FacialLogin';
import Registration from './Registration';

type AuthenticationProps = {
  navigation: any;
}

const Authentication:React.FC<AuthenticationProps> = ({ navigation }) => {
  const [index, setIndex] = useState(0);
  const [routes] = useState([
    { key: 'first', title: '使用帳號密碼登入' },
    { key: 'second', title: '使用臉部辨識登入' },
  ]);

  const layout = useWindowDimensions();

  return (
    <>
      <TabView
        navigationState={{ index, routes }}
        renderScene={SceneMap({
          first: () => <SimpleLogin navigation={navigation}/>,
          second: () => <FacialLogin navigation={navigation} />,
        })}
        onIndexChange={ setIndex } // Pass in the index to change index state: setIndex(index)
        initialLayout={{ width: layout.width }} />
    </>
  );
};

export default Authentication;
