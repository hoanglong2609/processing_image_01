import { useNavigation } from '@react-navigation/native';
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, StatusBar } from 'react-native';
import axios from 'axios';
import { API_URL } from './../constants';

const ResetPassword = () => {
  const navigation = useNavigation();
  const [code, setCode] = useState('');
  const [mail, setMail] = useState('');

  const handleLogin = async () => {
    if (code === "" || mail === "") {
      alert("Không được để trống mã code và email!");
      return;
    }
    await axios.get(`${API_URL}/user/forgot`, {
      params: {
        code: code,
        gmail: mail,
      }
    })
      .then(res => {
        console.log(res);

        alert("Vui lòng kiểm tra hòm thư của bạn");
      });

  };

  const handleRestPassword = () => {
    alert("Vui lòng liên hệ quản trị viên!");
  }

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" hidden={false} backgroundColor="#f2eef4" translucent={true} />
      <Text className="text-[28px] font-semibold text-[#413f52]">Quên mật khẩu</Text>
      <TextInput
        className="bg-white w-full h-[60px] rounded-lg px-3 mt-10"
        value={code}
        placeholder="Mã code"
        onChangeText={(text) => setCode(text)}
      />
      <TextInput
        className="bg-white w-full h-[60px] rounded-lg px-3 mt-5"
        value={mail}
        placeholder="Email nhận lại mật khẩu"
        onChangeText={(text) => setMail(text)}
      />

      <TouchableOpacity className="bg-[#fc6b68] w-full py-4 rounded-lg mt-8" onPress={handleLogin}>
        <Text className="text-center text-white text-[20px]">Gửi mail</Text>
      </TouchableOpacity>

      <TouchableOpacity className=" w-full py-4 rounded-lg mt-2" onPress={() => navigation.navigate('Login')}>
        <Text className="text-center text-gray-500 text-[18px]">Quay lại trang đăng nhập</Text>
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

export default ResetPassword;