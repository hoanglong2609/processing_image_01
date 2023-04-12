import { View, Text, StyleSheet, StatusBar, ScrollView, TouchableOpacity, ActivityIndicator, Image } from 'react-native';
import { Avatar, Icon } from '@rneui/themed';
import { AsyncStorage } from 'react-native';
import React, { useEffect, useState } from 'react';
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';
import { API_URL } from './../constants';

export default function Point() {
  const navigation = useNavigation();
  const [userId, setUserId] = useState("");
  const [subjectId, setSubjectId] = useState("");
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem('userId')
      .then(value => {
        setUserId(value);
      })

    AsyncStorage.getItem('subjectId')
      .then(value => {
        setSubjectId(value);
      })
  }, []);

  useEffect(() => {
    if (userId && subjectId) {
      getData()
    };
  }, [userId, subjectId]);

  const getData = async () => {
    await axios.get(`${API_URL}/score/`, {
      params: {
        student: userId,
        subject: subjectId
      }
    })
      .then(res => {
        setScores(res.data);
        setLoading(false);
      });
  }

  const viewResult = (code) => {
    if (!code) {
      alert("Không tìm thấy mã đề!!!")
    } else {
      AsyncStorage.setItem('codeExamp', code.toString());
      navigation.navigate('Result');
    }
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
            <Text className="text-[24px] font-semibold text-[#413f52] ml-2">Xem điểm </Text>
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
          {scores.length != 0 ?
            <>
              <TouchableOpacity
                className="bg-[#f36c6c] w-full p-3 rounded-xl flex h-[100px] mb-[15px]"
                style={{ flexDirection: 'row', alignItems: 'center' }}
              >
                <View
                  className="bg-[#fff] h-full w-[80px] rounded-lg mr-4"
                  style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}
                >
                  <Icon
                    size={50}
                    color='#f36c6c'
                    name='rule' />
                </View>
                <View className="text-center text-white text-[20px]">
                  <Text className="text-[23px] font-semibold text-gray-50">{scores[0].subject.name}</Text>
                  <Text className="text-[16px] font-semibold text-gray-100">{scores[0].student.name}</Text>
                </View>
              </TouchableOpacity>
              {scores.map((item, sindex) => (
                <View
                  key={`score${sindex}`}
                  className="bg-[#fff] w-full p-3 rounded-xl mb-[15px]"
                >
                  <View
                    className="mt-4"
                    style={{
                      flexDirection: 'row',
                      justifyContent: 'space-between',
                    }}
                  >
                    <View
                      style={{
                        flexDirection: 'row',
                        justifyContent: 'flex-start',
                      }}
                    >
                      <View className="text-center text-white text-[20px]">
                        <Text className="text-[16px] font-semibold text-gray-600">Mã đề: {item.code || "xxx"}</Text>
                        <Text className="text-[16px] font-semibold text-gray-500">Điểm số: {item.score}</Text>
                        <Text className="text-[16px] font-semibold text-gray-500">Đáp án đã chọn:</Text>
                        {item.filled_cell.map((point, index) => (
                          <Text key={`${sindex}-${index}`}>Câu {index + 1} : {point == 0 ? "A" : point == 1 ? "B" : point == 2 ? "C" : "D"}</Text>
                        ))}
                      </View>
                    </View>
                    <TouchableOpacity onPress={() => viewResult(item.code)}>
                      <View>
                        <Text className="text-[16px] font-semibold text-red-300 ml-2 italic">Xem đáp án</Text>
                      </View>
                    </TouchableOpacity>
                  </View>
                  <Text className="text-[16px] mt-4 font-semibold text-gray-500">Bài làm:</Text>
                  <Image
                    className="h-[315px] w-auto rounded-xl mb-10"
                    resizeMode="cover"
                    source={{
                      uri: item?.image?.url.replace('http://localhost:2100', API_URL)
                    }}
                    alt="Picture of result"
                  />
                </View>

              ))}

            </> :
            <View className="text-center text-white text-[20px]">
              <Text className="text-[16px] font-semibold text-gray-400 text-center mt-8">Chưa có điểm môn học này.</Text>
            </View>
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
