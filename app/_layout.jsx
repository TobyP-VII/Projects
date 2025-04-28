import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { Stack, Tabs } from 'expo-router'
import { Colors } from '../constants/colors'
import { StatusBar } from 'expo-status-bar'

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
                    tabBarActiveTintColor: Colors.iconColorFocused,
                    tabBarInactiveTintColor: Colors.iconColor,
                    
                }}
            >
                <Tabs.Screen name='index' options = {{title: 'Home'}}/>
                <Tabs.Screen name='picture' options = {{title: 'Picture'}}/>
                <Tabs.Screen name='signature' options = {{title: 'Signature'}}/>
            </Tabs>
        </>
    )
}

export default RootLayout

const styles = StyleSheet.create({})