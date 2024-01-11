import carla
import time

def print_filtered_blueprints(filter_word, world):
    # Get all blueprints that contain the filter word
    filtered_blueprints = [bp for bp in world.get_blueprint_library().filter("*" + filter_word + "*")]

    # Print the filtered blueprints
    print(f"Filtered Blueprints with '{filter_word}':")
    for blueprint in filtered_blueprints:
        print(blueprint.id)

    return filtered_blueprints


def spawn_objects(blueprint_array, origin_location, axis_direction, distance, world):
    # Define the spawn location
    spawn_location = carla.Location(*origin_location)

    # Normalize the axis direction vector
    axis_direction = carla.Vector3D(*axis_direction)

    # Array to store spawned actors
    spawned_actors = []

    # Spawn objects along the specified axis at the defined distance
    for index, blueprint_name in enumerate(blueprint_array):
        spawn_location += distance * axis_direction * index
        blueprint = world.get_blueprint_library().find(blueprint_name)
        actor = spawn_actor(world, blueprint, spawn_location)
        spawned_actors.append(actor)

    return spawned_actors


def spawn_actor(world, blueprint, spawn_location):
    # Spawn the actor
    transform = carla.Transform(spawn_location)
    actor = world.try_spawn_actor(blueprint, transform)

    if actor is not None:
        print(f"Spawned actor {actor.id} at {spawn_location}")
    else:
        print(f"Failed to spawn actor at {spawn_location}")

    return actor


def destroy_actors(actors):
    # Destroy the spawned actors
    for actor in actors:
        if actor is not None:
            actor.destroy()
            print(f"Destroyed actor {actor.id}")


# Example usage
if __name__ == "__main__":
    # Create a CARLA client
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Get the CARLA world
    world = client.get_world()
    
    print_filtered_blueprints('plane', world)


    # Define the axis direction (x, y, z)
    axis_direction = (0.0, 1.0, 0.0)  # Along the x-axis

    
    plane_blueprints = [
        #'static.prop.plane_a320_v01',
       # 'static.prop.plane_a320_v02',
       # 'static.prop.plane_a340_v02',
       # 'static.prop.plane_a340_v01',
        #'static.prop.plane_boeing_737_v01',
        'static.prop.plane_boeing_747_v01'
    ]

    # Define the birds blueprint array
    birds_blueprint_array = [
        'static.prop.bird_september_14',
        'static.prop.bird_september_11',
        'static.prop.bird_september_17',
        'static.prop.bird_september_16',
        'static.prop.bird_september_13',
        'static.prop.bird_september_15',
        'static.prop.bird_september_12',
    ]

    # Define the drones blueprint array
    drones_blueprint_array = [
        'static.prop.drone_civilian_generic',
        'static.prop.drone_fictitious_cyberpolicevtol',
        'static.prop.drone_civilian_bee',
        'static.prop.drone_civilian_minimalistic',
        'static.prop.drone_swan',
        'static.prop.drone_civilian_phantom',
        'static.prop.drone_civilian_parrot',
        'static.prop.drone_fiveinch',
        'static.prop.drone_450',
        'static.prop.drone_x500'
    ]
    
    bayraktar_blueprint_array = [
        'static.prop.drone_military_bayraktar']
        
    reaper_blueprint_array = [
        'static.prop.drone_military_reaper']
        
     # Define the base origin location
    base_origin_location = (-81.0, 68.0, 26.5)   
    base_origin_location = (-164.0, 163.0, 20.5)

     # Spawn birds and derive positions for drones, bayraktar drones, and reaper drones
    spawned_birds = spawn_objects(birds_blueprint_array, base_origin_location, axis_direction, 0.8, world)

    # Derive positions for drones, bayraktar drones, and reaper drones from the position of spawned_birds  
    
    offset_drones = tuple(x + y for x, y in zip(base_origin_location, (5.0, 0.0, 0.0)))
    offset_bayraktar = tuple(x + y for x, y in zip(base_origin_location, (6.0, -12.0, 0.0)))
    offset_reaper = tuple(x + y for x, y in zip(base_origin_location, (12.0, -4.0, 0.0)))
    offset_planes = tuple(x + y for x, y in zip(base_origin_location, (30.0, -30.0, 20.0)))

    spawned_drones = spawn_objects(drones_blueprint_array, offset_drones  , axis_direction, 0.5, world)
    bayraktar_drones = spawn_objects(bayraktar_blueprint_array, offset_bayraktar  , axis_direction, 10, world)
    reaper_drones = spawn_objects(reaper_blueprint_array, offset_reaper , axis_direction, 10, world)
    planes = spawn_objects(plane_blueprints, offset_planes , axis_direction, 10, world)

    # Wait for 5 seconds
    time.sleep(5)

    # Destroy the spawned actors and terminate the program
    destroy_actors(spawned_birds)
    destroy_actors(spawned_drones)
    destroy_actors(bayraktar_drones)
    destroy_actors(reaper_drones)
    destroy_actors(planes)

