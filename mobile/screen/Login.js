import { useNavigation } from '@react-navigation/native';
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, StatusBar, Image } from 'react-native';
import { AsyncStorage } from 'react-native';
import axios from 'axios';
import { API_URL } from './../constants';

const Login = () => {
  const navigation = useNavigation();
  const [code, setCode] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    if (code === "" || password === "") {
      alert("Không được để trống tài khoản hoặc mật khẩu!");
      return;
    }
    await axios.post(`${API_URL}/user/login`, {
      code: code,
      password: password,
    })
      .then(res => {
        if (res.data.code === 200) {
          AsyncStorage.setItem('userId', res.data.data.id.toString());
          AsyncStorage.setItem('subjects', JSON.stringify(res.data.data.subjects));
          AsyncStorage.setItem('userLogin', res.data.data.name);
          AsyncStorage.setItem('role', res.data.data.role.toString());
          navigation.navigate('Dashbroad');

        } else {
          alert("Sai tài khoản hoạc mật khẩu");
        }
      });
  };

  const handleRestPassword = () => {
    navigation.navigate('ResetPassword');

  }

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" hidden={false} backgroundColor="#f2eef4" translucent={true} />
      <Image
        className="h-[140px] w-[140px] rounded-full"
        resizeMode="cover"
        source={require('./../assets/logo.png')}
      />
      <Text className="text-[28px] font-semibold text-[#413f52] mt-6">Đăng nhập</Text>
      <TextInput
        className="bg-white w-full h-[60px] rounded-lg px-3 mt-10"
        value={code}
        placeholder="Mã code"
        onChangeText={(text) => setCode(text)}
      />
      <TextInput
        className="bg-white w-full h-[60px] rounded-lg px-3 mt-5"
        value={password}
        placeholder="Mật khẩu"
        secureTextEntry={true}
        onChangeText={(text) => setPassword(text)}
      />
      <TouchableOpacity className="w-full mt-2" onPress={handleRestPassword}>
        <Text className="text-right text-gray-500 text-[13px]">Quên mật khẩu</Text>
      </TouchableOpacity>
      <TouchableOpacity className="bg-[#fc6b68] w-full py-4 rounded-lg mt-8" onPress={handleLogin}>
        <Text className="text-center text-white text-[20px]">Đăng nhập</Text>
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

export default Login;