import React, { useState } from "react";
import React, { useRef } from "react";
import { useGLTF } from "@react-three/drei";

export function Model(props) {
  const { nodes, materials } = useGLTF("/old_crt_monitor_model.glb");
  return (
    <group {...props} dispose={null}>
      <group rotation={[-Math.PI / 2, 0, 0.635]} scale={0.128}>
        <group rotation={[Math.PI / 2, 0, 0]}>
          <mesh
            castShadow
            receiveShadow
            geometry={nodes.Object_4.geometry}
            material={materials.ONWindow}
            scale={[1.776, 1.697, 2.409]}
          />
        </group>
      </group>
    </group>
  );
}

useGLTF.preload("/old_crt_monitor_model.glb");
