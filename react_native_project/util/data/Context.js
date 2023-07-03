import React, { useState } from 'react';

const AuthContext = React.createContext({
  isLoggedIn: false,
  currentUser: '',
});

export const ContextProvider = (props) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  return (
    <AuthContext.Provider value={{
      isLoggedIn: isLoggedIn,
      currentUser: currentUser,
    }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
