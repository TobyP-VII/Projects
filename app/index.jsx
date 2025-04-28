import { Pressable, StyleSheet, Text, View } from 'react-native'
import React from 'react'
import ThemedView from '../components/ThemedView'
import Spacer from '../components/Spacer'
import { Link } from 'expo-router'
import styles from '../constants/styles'
import ThemedButton from '../components/ThemedButton'

const Home = () => {

    const handleOpenCam = () => {
        console.log('opening camera')
    }

    return (
        <ThemedView>

            <Text>
                Here is text
            </Text>

            <Spacer/>
            <ThemedButton onPress={handleOpenCam}>
                <Text>
                    Take picture
                </Text>
            </ThemedButton>
            <Spacer/>

            <Text>
                Here is text
            </Text>

        </ThemedView>
    )
}

export default Home
