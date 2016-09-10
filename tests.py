from main import SPRITE_SIZE, WIDTH, HEIGHT
from main import Rect, Entity, Player
from main import entities, collisions, load_sprites
import unittest


def init():
    load_sprites()

class RectTestCase(unittest.TestCase):

    def setUp(self):
        self.r1 = Rect(0, 0, 10, 10)
        self.r2 = Rect(5, 5, 15, 15)
        self.r3 = Rect(20, 20, 40, 40)

    def tearDown(self):
        pass

    def test_overlaps_trueForOverlappingRectangles(self):
        self.assertTrue(self.r1.overlaps(self.r2))

    def test_overlaps_falseForNonOverlappingRectangles(self):
        self.assertFalse(self.r1.overlaps(self.r3))

    def test_overlaps_methodIsCommutativeForOverlappingRectangles(self):
        self.assertEqual(self.r1.overlaps(self.r2), self.r2.overlaps(self.r1))

    def test_overlaps_methodIsCommutativeForNonOverlappingRectangles(self):
        self.assertEqual(self.r1.overlaps(self.r2), self.r2.overlaps(self.r1))


class EntityTestCase(unittest.TestCase):

    def setUp(self):
        entities.clear()
        collisions.clear()

    def tearDown(self):
        pass

    def test_checkCollisions_collisionsListContainsCollidedEntities(self):
        entityToTest = Entity()
        entityCollidedWith = Entity()
        entities.append(entityCollidedWith)
        entityToTest.check_collisions()
        self.assertListEqual(collisions, [(entityToTest, entityCollidedWith)])

    def test_checkCollisions_entityDoesNotCollideWithSelf(self):
        entityToTest = Entity()
        entities.append(entityToTest)
        entityToTest.check_collisions()
        self.assertFalse(collisions)

    def test_checkCollisions_emptyCollisionsListWhenNoOtherEntities(self):
        entityToTest = Entity()
        entityToTest.check_collisions()
        self.assertFalse(collisions)

    def test_checkCollisions_oneCollisionDetectedWhenMultipleEntitiesPresent(self):
        entityToTest, collidedEntity = Entity(), Entity()
        distantEntity1, distantEntity2 = Entity(), Entity()
        distantEntity1.x, distantEntity1.y = 500, 500
        distantEntity2.x, distantEntity2.y = 800, 800
        entities.extend([collidedEntity, distantEntity1, distantEntity2])
        entityToTest.check_collisions()
        self.assertListEqual(collisions, [(entityToTest, collidedEntity)])

    def test_checkCollisions_emptyCollisionsListWhenOtherEntityXPosGreaterThanSpriteSize(self):
        entityToTest, otherEntity = Entity(), Entity()
        otherEntity.x += SPRITE_SIZE+1
        entities.append(otherEntity)
        entityToTest.check_collisions()
        self.assertFalse(collisions)

    def test_checkCollisions_oneCollisionDetectedWhenOtherEntityXPosLessThanSpriteSize(self):
        entityToTest, otherEntity = Entity(), Entity()
        otherEntity.x += SPRITE_SIZE-1
        entities.append(otherEntity)
        entityToTest.check_collisions()
        self.assertListEqual(collisions, [(entityToTest, otherEntity)])

    def test_checkCollisions_emptyCollisionsListWhenOtherEntityXPosEqualsSpriteSize(self):
        entityToTest, otherEntity = Entity(), Entity()
        otherEntity.x += SPRITE_SIZE
        entities.append(otherEntity)
        entityToTest.check_collisions()
        self.assertFalse(collisions)

    def test_insideXBoundary_falseWhenEntityXPosIsNegative(self):
        entityToTest = Entity()
        entityToTest.x = -1
        self.assertFalse(entityToTest.inside_x_boundary())

    def test_insideXBoundary_falseWhenEntityXPosGreaterThanScreenWidth(self):
        entityToTest = Entity()
        entityToTest.x = WIDTH + 1
        self.assertFalse(entityToTest.inside_x_boundary())

    def test_insideYBoundary_falseWhenEntityYPosIsNegative(self):
        entityToTest = Entity()
        entityToTest.y = -1
        self.assertFalse(entityToTest.inside_y_boundary())

    def test_insideXBoundary_falseWhenEntityYPosGreaterThanScreenHeight(self):
        entityToTest = Entity()
        entityToTest.y = HEIGHT + 1
        self.assertFalse(entityToTest.inside_y_boundary())



class PlayerTestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def tearDown(self):
        pass

    def test_accelerate_successfulWithLowTemperatureAndVelocity(self):
        oldVelocity = self.player.velocity
        self.player.accelerate()
        self.assertFalse(self.player.velocity == oldVelocity)

    def test_accelerate_failsWhenMaxVelocityExceeded(self):
        self.player.velocity += self.player.max_velocity
        oldVelocity = self.player.velocity
        self.player.accelerate()
        self.assertTrue(self.player.velocity == oldVelocity)

    def test_accelerate_failsWhenMaxTemperatureExceeded(self):
        self.player.temperature += self.player.max_temperature
        oldTemperature = self.player.temperature
        self.player.accelerate()
        self.assertTrue(self.player.temperature == oldTemperature)

    def test_accelerate_temperatureUnchangedOnFailDueToExcessiveVelocity(self):
        self.player.velocity = self.player.max_velocity+1
        oldTemperature = self.player.temperature
        self.player.accelerate()
        self.assertTrue(self.player.temperature == oldTemperature)

    def test_accelerate_temperatureUnchangedOnFailDueToExcessiveTemperature(self):
        self.player.temperature = self.player.max_temperature+1
        oldTemperature = self.player.temperature
        self.player.accelerate()
        self.assertTrue(self.player.temperature == oldTemperature)

    def test_decelerate_successfulWithLowTemperatureAndVelocity(self):
        oldVelocity = self.player.velocity
        self.player.decelerate()
        self.assertFalse(self.player.velocity == oldVelocity)

    def test_decelerate_failsWhenMinVelocityExceeded(self):
        self.player.velocity = self.player.min_velocity-1
        oldVelocity = self.player.velocity
        self.player.decelerate()
        self.assertTrue(self.player.velocity == oldVelocity)

    def test_decelerate_failsWhenMaxTemperatureExceeded(self):
        self.player.temperature += self.player.max_temperature
        oldTemperature = self.player.temperature
        self.player.decelerate()
        self.assertTrue(self.player.temperature == oldTemperature)

    def test_decelerate_temperatureUnchangedOnFailDueToLowVelocity(self):
        self.player.velocity = self.player.min_velocity-1
        oldTemperature = self.player.temperature
        self.player.decelerate()
        self.assertTrue(self.player.temperature == oldTemperature)

    def test_decelerate_temperatureUnchangedOnFailDueToExcessiveTemperature(self):
        self.player.temperature = self.player.max_temperature+1
        oldTemperature = self.player.temperature
        self.player.decelerate()
        self.assertTrue(self.player.temperature == oldTemperature)


class AsteroidTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class BulletTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass



if __name__ == '__main__':
    init()
    unittest.main()