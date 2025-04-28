import { View } from 'react-native'
import { Colors } from '../constants/colors'
import React from 'react'

const ThemedView = ({style, ...props}) => {
    return (
        <View 
            style={[{
                flex: 1,
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: Colors.background,
            },
            style
            ]}
            {...props}
        />
    )
}

export default ThemedView