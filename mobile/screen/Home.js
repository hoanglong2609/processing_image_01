import React from 'react';
import { Text, StyleSheet, Image, TouchableOpacity, View } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StatusBar } from 'react-native'
import { NativeBaseProvider, Box, AspectRatio } from "native-base";

const Home = () => {
  const navigation = useNavigation();

  return (
    <NativeBaseProvider>
      <StatusBar barStyle="dark-content" hidden={false} backgroundColor="#f2eef4" translucent={true} />
      <Box style={styles.container}>
        <Image
          className="h-[50%] w-full rounded-2xl"
          resizeMode="cover"
          source={{
            uri: "https://images.unsplash.com/photo-1544716278-e513176f20b5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTR8fGJvb2t8ZW58MHx8MHx8&auto=format&fit=crop&w=500&q=60"
          }}
          alt="Picture of a Flower"
        />

        <View className="h-[30%]">
          <Text className="text-[30px] text-center font-semibold mt-[40px] text-[#413f52]">Manager Exam</Text>
          <Text className="text-[30px] text-center font-semibold mt-[10px] text-[#413f52]">Make it Easy and Quick!</Text>
        </View>

        <TouchableOpacity className="bg-yellow-400 px-14 py-4 rounded-lg mt-[15%]" onPress={() => navigation.navigate('Login')}>
          <Text className="text-white text-[20px] font-semibold">Join Now</Text>
        </TouchableOpacity>
      </Box>
    </NativeBaseProvider>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingTop: 30,
    paddingLeft: 12,
    paddingRight: 12,
    flex: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    backgroundColor: "#f2eef4",
    position: "relative"
  }
});

export default Home; 