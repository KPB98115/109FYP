import React from 'react';
import { View, Button, Modal, Text, StyleSheet } from 'react-native';

type CustomModalProps = {
  modalText: string;
  isButtonAppear: boolean;
  modalCallback: () => void;
}

const CustomModal: React.FC<CustomModalProps> = ({ modalText, isButtonAppear, modalCallback }) => {

  return (<View style={styles.modalContainer}>
    <Modal visible={true} animationType="slide" transparent={true}>
      <View style={styles.centeredView}>
        <View style={styles.modalView}>
          <Text style={styles.modalText}>{modalText}</Text>
          { isButtonAppear && <Button title={'close'} onPress={ modalCallback } /> }
        </View>
      </View>
    </Modal>
  </View>);
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
    alignContent: 'center',
  },
  modalContainer: {
    position: 'absolute',
  },
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22,
  },
  modalView: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalText: {
    marginBottom: 15,
    textAlign: 'center',
  },
});

export default CustomModal;
