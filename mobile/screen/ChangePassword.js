import { useNavigation } from '@react-navigation/native';
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, StatusBar, Alert } from 'react-native';
import axios from 'axios';
import { API_URL } from './../constants';
import { useEffect } from 'react';
import { AsyncStorage } from 'react-native';

const ChangePassword = () => {
  const navigation = useNavigation();
  const [userId, setUserId] = useState(null);
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newConfirmPassword, setNewConfirmPassword] = useState('');

  useEffect(() => {
    AsyncStorage.getItem('userId')
      .then(value => {
        setUserId(Number(value));
      })
  }, []);

  
  const handleChangePassword = async () => {
    if (oldPassword === "" || newPassword === "" || newConfirmPassword === "") {
      alert("Không được để trống các trường 😀!");
      return;
    }
    if (newPassword !== newConfirmPassword) {
      alert("password confirm không khớp 😀!");
      return;
    }
    await axios.post(`${API_URL}/user/change_password`, {
      id: userId,
      old_password: oldPassword,
      new_password: newPassword
    })
      .then(res => {
        console.log(res);

        Alert.alert("Success !!!", "Thay đổi mật khẩu thành công 😀", [
          {
            text: "Quay về trang chủ",
            onPress: () => {
              navigation.navigate('Dashbroad');
            }
          }
        ]);
      });

  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" hidden={false} backgroundColor="#f2eef4" translucent={true} />
      <Text className="text-[28px] font-semibold text-[#413f52]">Đổi mật khẩu</Text>
      <TextInput
        className="bg-white w-full h-[60px] rounded-lg px-3 mt-10"
        value={oldPassword}
        placeholder="Mật khẩu cũ"
        onChangeText={(text) => setOldPassword(text)}
      />
      <TextInput
        className="bg-white w-full h-[60px] rounded-lg px-3 mt-5"
        value={newPassword}
        placeholder="Nhập mật khẩu mới"
        onChangeText={(text) => setNewPassword(text)}
      />
      <TextInput
        className="bg-white w-full h-[60px] rounded-lg px-3 mt-5"
        value={newConfirmPassword}
        placeholder="Nhập lại mật khẩu mới"
        onChangeText={(text) => setNewConfirmPassword(text)}
      />

      <TouchableOpacity className="bg-[#fc6b68] w-full py-4 rounded-lg mt-8" onPress={handleChangePassword}>
        <Text className="text-center text-white text-[20px]">Xác nhận</Text>
      </TouchableOpacity>

      <TouchableOpacity className=" w-full py-4 rounded-lg mt-2" onPress={() => navigation.navigate('Dashbroad')}>
        <Text className="text-center text-gray-500 text-[18px]">Quay lại</Text>
      </TouchableOpacity>
    </View>
  );
};


const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f2eef4',
    padding: 20,
  },
});

export default ChangePassword;