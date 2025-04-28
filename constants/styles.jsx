import { StyleSheet, Text, View } from 'react-native'
import { Colors } from '../constants/colors'

const styles = StyleSheet.create({
    btn: {
        backgroundColor: Colors.iconColor,
        padding: 15,
        borderRadius: 5,
    },
    pressed: {
        opacity: 0.8,
    },
})

export default styles