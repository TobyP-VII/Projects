import { Pressable } from 'react-native'
import styles from '../constants/styles'
import React from 'react'

const ThemedButton = ({style, ...props}) => {
    return (
        <Pressable
            style={({pressed}) => [styles.btn, pressed && styles.pressed, style]}
            {...props}
        />
    )
}

export default ThemedButton