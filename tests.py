from main import SPRITE_SIZE
from main import Rect, Entity
from main import entities, collisions
import unittest


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


class PlayerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


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
    unittest.main()