import { View, Text, StyleSheet, StatusBar, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Icon } from '@rneui/themed';
import { AsyncStorage } from 'react-native';
import React, { useEffect, useState } from 'react';
import { useNavigation } from '@react-navigation/native';
import axios from 'axios';
import { API_URL } from './../constants';

export default function ListStudent() {
  const navigation = useNavigation();
  const [subjectName, setSubjectName] = useState("");
  const [subjectId, setSubjectId] = useState("");
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem('subjectName')
      .then(value => {
        setSubjectName(value);
      })

    AsyncStorage.getItem('subjectId')
      .then(value => {
        setSubjectId(value);
      })
  }, []);

  useEffect(() => {
    if (subjectId) {
      getData()
    };
  }, [subjectId]);

  const getData = async () => {
    await axios.get(`${API_URL}/user/`, {
      params: {
        subject: subjectId
      }
    })
      .then(res => {
        const data = res.data.filter((item) => item.role == 0);

        setStudents(data);
        setLoading(false);
      });
  }

  const handViewPoint = (studentId) => {
    AsyncStorage.setItem('userId', studentId.toString());
    navigation.navigate('Point');

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
        <View>
          <Text className="text-[26px] font-semibold text-[#413f52] ml-2">{subjectName}</Text>
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
            <Text className="ml-2 text-[20px] font-semibold text-gray-600 mb-3">Sĩ số: {students.length}</Text>
          </View>
          {students.map((item) => (
            <TouchableOpacity
              onPress={() => handViewPoint(item.id)}
              key={item.id}
              className="bg-[#fff] w-full p-3 rounded-xl flex h-[80px] mb-[15px]"
              style={{ flexDirection: 'row', alignItems: 'center' }}
            >
              <Icon
                size={45}
                name='sc-telegram'
                type='evilicon'
                color='#ff914c'
              />
              <View className="text-center text-white text-[16px] mt-2">
                <Text className="text-[18px] font-semibold text-gray-600">{item.name}</Text>
              </View>
            </TouchableOpacity>
          ))
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
