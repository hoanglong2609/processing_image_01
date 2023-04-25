import { View, Text, StyleSheet, StatusBar, ScrollView, TouchableOpacity, Alert, BackHandler } from 'react-native';
import { Avatar, Icon } from '@rneui/themed';
import { AsyncStorage } from 'react-native';
import React, { useEffect, useState } from 'react';
import { useNavigation } from '@react-navigation/native';

export default function Dashbroad() {
  const navigation = useNavigation();
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [subject, setSubject] = useState([]);

  useEffect(() => {
    const backAction = () => {
      if (navigation.isFocused()) {
        Alert.alert("Xác nhận đăng xuất", "Bạn có chắc chắn muốn đăng xuất khỏi ứng dụng?", [
          {
            text: "Không",
            onPress: () => null,
            style: "cancel"
          },
          {
            text: "Có",
            onPress: () => {
              navigation.navigate('Login');
            }
          }
        ]);
        return true;
      } else {
        return false;
      }
    };

    const backHandler = BackHandler.addEventListener(
      "hardwareBackPress",
      backAction
    );

    return () => backHandler.remove();
  }, [navigation]);

  useEffect(() => {
    AsyncStorage.getItem('subjects')
      .then(value => {
        setSubject(JSON.parse(value));
      })

    AsyncStorage.getItem('userLogin')
      .then(value => {
        setName(value);
      })

    AsyncStorage.getItem('role')
      .then(value => {
        if (value == 1) {
          setRole("Giảng viên");
          return;
        }
        setRole("Học viên");
      })
  }, []);

  const logOut = () => {
    Alert.alert("Xác nhận đăng xuất", "Bạn có chắc chắn muốn đăng xuất khỏi ứng dụng?", [
      {
        text: "Không",
        onPress: () => null,
        style: "cancel"
      },
      {
        text: "Có",
        onPress: () => {
          navigation.navigate('Login');
        }
      }
    ]);
  }

  const handViewPoint = (subjectId, subjectName) => {
    AsyncStorage.setItem('subjectId', subjectId.toString());
    AsyncStorage.setItem('subjectName', subjectName);
    if (role == "Học viên") {
      navigation.navigate('Point');
    } else {
      navigation.navigate('ListStudent');
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
          <Avatar
            size={55}
            rounded
            title={name.substring(0, 2).toUpperCase()}
            containerStyle={{ backgroundColor: "pink" }}
          />
          <View>
            <Text className="text-[26px] font-semibold text-[#413f52] ml-2">{name}</Text>
            <Text className="text-[14px] font-semibold text-[#717177] ml-2">{role}</Text>
          </View>
        </View>

        <View
          style={{
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <Icon
            onPress={() => navigation.navigate('ChangePassword')}
            size={35}
            color='#413f52'
            name='key-outline'
            type='ionicon'
          />
          <View className="ml-4">
            <Icon
              onPress={logOut}
              size={35}
              color='#413f52'
              name='exit-outline'
              type='ionicon'
            />
          </View>
        </View>
        
      </View>
      <View
        className="h-[200px] bg-[#252d56] rounded-xl mb-[30px]"
        style={{
          flexDirection: 'row',
          justifyContent: 'space-between',
        }}
      >
        <View className="w-[50%] py-4 rounded-xl">
          <Text className="text-gray-100 mt-[33%] text-center text-[20px] uppercase font-extrabold">total {subject.length}</Text>
          <Text className="text-gray-100 text-center text-[16px] uppercase ">class</Text>
        </View>
        <View className="w-[50%] py-4 rounded-xl">
          <Text className=" text-gray-100 mt-[33%] text-center text-[20px] uppercase font-extrabold">Have 5</Text>
          <Text className=" text-gray-100 text-center text-[16px] uppercase ">exam</Text>
        </View>
      </View>
      <View >
        <Text className="text-[23px] font-semibold text-gray-600 mb-4">Danh sách các lớp học</Text>
      </View>

      {subject.map((item) => (
        <TouchableOpacity
          onPress={() => handViewPoint(item.id, item.name)}
          key={item.id}
          className="bg-[#fff] w-full p-3 rounded-xl flex h-[100px] mb-[15px]"
          style={{ flexDirection: 'row', alignItems: 'center' }}
        >
          <View
            className="bg-[#5181e9] h-full w-[80px] rounded-lg mr-4"
            style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}
          >
            <Icon
              size={45}
              color='#fff'
              name='class' />
          </View>
          <View className="text-center text-white text-[20px]">
            <Text className="text-[23px] font-semibold text-gray-600">{item.name}</Text>
            <Text className="text-[14px] font-semibold text-gray-400">View point in class.</Text>
          </View>
        </TouchableOpacity>
      ))}
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
