import 'react-native-gesture-handler';
import { StyleSheet, LogBox } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Home from './screen/Home';
import Login from './screen/Login';
import Dashbroad from './screen/Dashbroad';
import Point from './screen/Point';
import Result from './screen/Result';
import ListStudent from './screen/ListStudent';
import ResetPassword from './screen/ForgotPassword';
import ChangePassword from './screen/ChangePassword';
LogBox.ignoreAllLogs();//Ignore all log notifications

export default function App() {
  const Stack = createStackNavigator();

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={Home}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
        <Stack.Screen
          name="Login"
          component={Login}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
        <Stack.Screen
          name="ResetPassword"
          component={ResetPassword}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
        <Stack.Screen
          name="Dashbroad"
          component={Dashbroad}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
        <Stack.Screen
          name="ChangePassword"
          component={ChangePassword}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
        <Stack.Screen
          name="ListStudent"
          component={ListStudent}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
        <Stack.Screen
          name="Point"
          component={Point}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
        <Stack.Screen
          name="Result"
          component={Result}
          options={{
            headerMode: 'none',
            navigationOptions: {
              headerVisible: false,
            }
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
