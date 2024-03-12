import React, { useState } from 'react';

const AuthContext = React.createContext({
  isLoggedIn: false,
  currentUser: '',
  isRestricted: false,
  selectedURL: '',
});

export const ContextProvider = (props) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState('');
  const [isRestricted, setIsRestricted] = useState(false);
  const [selectedURL, setSelectedURL] = useState('');

  return (
    <AuthContext.Provider value={{
      isLoggedIn: isLoggedIn,
      currentUser: currentUser,
      isRestricted: isRestricted,
      selectedURL: selectedURL,
    }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
