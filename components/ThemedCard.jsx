import { View } from 'react-native'
import { Colors } from '../constants/colors'
import React from 'react'

const ThemedCard = ({style, ...props}) => {
    return (
        <View
            style={[{
                backgroundColor: Colors.uiBackground,
                borderRadius: 5,
                padding: 20,
            },
            style
            ]}
            {...props}
        />
    )
}

export default ThemedCard