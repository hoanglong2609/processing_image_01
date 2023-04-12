import { View, Text, StyleSheet, StatusBar, ScrollView, Image, ActivityIndicator, TouchableOpacity } from 'react-native';
import { Icon } from '@rneui/themed';
import { AsyncStorage } from 'react-native';
import React, { useEffect, useState } from 'react';
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';
import { API_URL } from './../constants';

export default function Result() {
  const navigation = useNavigation();
  const [codeExamp, setCodeExamp] = useState("");
  const [result, setResult] = useState();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem('codeExamp')
      .then(value => {
        setCodeExamp(value);
      })

  }, []);

  useEffect(() => {
    if (codeExamp) {
      getData()
    };
  }, [codeExamp]);

  const getData = async () => {
    await axios.get(`${API_URL}/result/`)
      .then(res => {
        const _result = res.data.find((item) => item.code == codeExamp);
        setResult(_result);
        setLoading(false);
      });
  }

  return (
    <ScrollView style={styles.container} className="px-[4%]" contentContainerStyle={{ paddingBottom: 50 }}>
      <StatusBar barStyle="dark-content" hidden={false} backgroundColor="#f2eef4" translucent={true} />
      <View
        className="mt-[25px] mb-[20px]"
        style={{
          flexDirection: 'row',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <View
          style={{
            flexDirection: 'row',
            justifyContent: 'flex-start',
            alignItems: 'center'
          }}
        >
          <View>
            <Text className="text-[24px] font-semibold text-[#413f52] ml-2">Đáp án đúng</Text>
          </View>
        </View>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Icon
            size={35}
            color='#413f52'
            name='arrow-back-outline'
            type='ionicon'
          />
        </TouchableOpacity>
      </View>
      {loading ?
        <ActivityIndicator size="large" color="#0000ff" /> :
        <>
          <View className="text-center text-white text-[20px]">
            <Text className="ml-2 text-[18px] font-semibold text-gray-600 italic mb-4">Mã đề: {result && result?.code || ""}</Text>
          </View>

          <View className="bg-[#fff] w-full p-3 rounded-xl mb-[15px]">
            {result && result.result.map((point, index) => (
              <Text key={index}>Câu {index + 1} : {point == 0 ? "A" : point == 1 ? "B" : point == 2 ? "C" : "D"}</Text>
            ))}
          </View>

          <View className="text-center text-white text-[20px]">
            <Text className="ml-2 text-[18px] font-semibold text-gray-600 italic mb-4">Ảnh minh họa</Text>
          </View>

          {result &&
            <Image
              className="h-[315px] w-auto rounded-xl mb-10"
              resizeMode="cover"
              source={{
                uri: result?.image?.url.replace('http://localhost:2100', API_URL)
              }}
              alt="Picture of result"
            />
          }
        </>
      }
    </ScrollView >
  )
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 40,
    flex: 1,
    backgroundColor: "#f2eef4",
    position: "relative",
  }
});
