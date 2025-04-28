import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { Stack, Tabs } from 'expo-router'
import { Colors } from '../constants/colors'
import { StatusBar } from 'expo-status-bar'
import { Ionicons } from '@expo/vector-icons'

const RootLayout = () => {
    
    return (
        <>
            <StatusBar value='auto' />
            <Tabs 
                screenOptions={{
                    headerShown: false,
                    tabBarStyle: {
                        backgroundColor: Colors.navBackground,
                        paddingTop: 10,
                        height: 80,
                    },
                    tabBarInactiveTintColor: Colors.iconColor,
                    tabBarActiveTintColor: Colors.iconColor,
                    
                }}
            >
                <Tabs.Screen
                    name='index'
                    options = {{title: 'Home', tabBarIcon: ({focused}) => (
                        <Ionicons 
                            size={32}
                            name={focused ? 'home' : 'home-outline'}
                            color={Colors.iconColor}
                        />
                    ) }}
                />
                <Tabs.Screen
                    name='picture'
                    options = {{title: 'Picture', tabBarIcon: ({focused}) => (
                        <Ionicons 
                            size={32}
                            name={focused ? 'camera' : 'camera-outline'}
                            color={Colors.iconColor}
                        />
                    ) }}
                />
                <Tabs.Screen
                    name='signature'
                    options = {{title: 'Signature', tabBarIcon: ({focused}) => (
                        <Ionicons 
                            size={32}
                            name={focused ? 'checkmark-circle' : 'checkmark-circle-outline'}
                            color={Colors.iconColor}
                        />
                    ) }}
                />
            </Tabs>
        </>
    )
}

export default RootLayout

const styles = StyleSheet.create({})